import { useEffect, useState } from 'react'
import api from '../api'

export default function ProfilePage() {
  const [profile, setProfile] = useState({ department: '', designation: '' })

  const fetchProfile = async () => {
    try {
      const res = await api.get('/user/profile')
      setProfile(res.data || { department: '', designation: '' })
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to load profile')
    }
  }

  useEffect(() => {
    fetchProfile()
  }, [])

  const saveProfile = async () => {
    try {
      await api.put('/user/profile', profile)
      await fetchProfile()
      alert('Profile saved')
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to save profile')
    }
  }


  return (
    <div className="page">
      <h2>Profile</h2>
      <div className="profile-section">
        <input
          placeholder="Department"
          value={profile.department || ''}
          onChange={(e) => setProfile({ ...profile, department: e.target.value })}
        />
        <input
          placeholder="Designation"
          value={profile.designation || ''}
          onChange={(e) => setProfile({ ...profile, designation: e.target.value })}
        />
        <button onClick={saveProfile}>Save Profile</button>
      </div>

    </div>
  )
}
