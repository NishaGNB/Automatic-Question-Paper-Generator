import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  return (
    <div className="page">
      <h1>Welcome, {user?.name}</h1>
      <p>Generate intelligent exam question papers using your syllabus & references.</p>
      <div className="cards">
        <Link to="/generate" className="card">
          Generate Question Paper
        </Link>
        <Link to="/papers" className="card">
          View Generated Papers
        </Link>
        <Link to="/profile" className="card">
          Profile & Uploads
        </Link>
      </div>
    </div>
  )
}
