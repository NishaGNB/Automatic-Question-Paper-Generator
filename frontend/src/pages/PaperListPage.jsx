import { useEffect, useState } from 'react'
import api from '../api'

export default function PaperListPage() {
  const [papers, setPapers] = useState([])

  const fetchPapers = async () => {
    try {
      const res = await api.get('/papers')
      setPapers(res.data)
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to load papers')
    }
  }

  useEffect(() => {
    fetchPapers()
  }, [])

  return (
    <div className="page">
      <h2>Generated Question Papers</h2>
      {papers.length === 0 && <p>No papers generated yet.</p>}
      <div className="papers-list">
        {papers.map((p) => (
          <div key={p.id} className="paper-card">
            <h4>
              {p.subject} ({p.subject_code}) - Set {p.set_number}
            </h4>
            <p>Semester: {p.semester}</p>
            <p>Total Marks: {p.total_marks}</p>
            <ul>
              {p.questions.map((q) => (
                <li key={q.id}>
                  <strong>M{q.module_number}</strong> [{q.marks} marks] ({q.blooms_level}) -{' '}
                  {q.question_text}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  )
}
