import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <span className="logo">Smart Question Paper Generator</span>
      </div>
      <div className="navbar-right">
        {user ? (
          <>
            <Link to="/">Dashboard</Link>
            <Link to="/generate">Generate Paper</Link>
            <Link to="/papers">Generated Papers</Link>
            <Link to="/profile">Profile</Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}
