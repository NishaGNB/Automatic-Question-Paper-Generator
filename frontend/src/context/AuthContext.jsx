import { createContext, useContext, useEffect, useState } from 'react'
import api from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  const fetchMe = async () => {
    try {
      const res = await api.get('/user/me')
      setUser(res.data)
    } catch {
      setUser(null)
    }
  }

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchMe()
    }
  }, [])

  const login = async (email, password) => {
    const res = await api.post('/auth/login', { email, password })
    localStorage.setItem('access_token', res.data.access_token)
    await fetchMe()
  }

  const signup = async (name, email, password) => {
    await api.post('/auth/signup', { name, email, password })
    await login(email, password)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
