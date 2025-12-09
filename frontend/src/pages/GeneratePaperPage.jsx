import { useState } from 'react'
import api from '../api'
import ModuleForm from '../components/ModuleForm'

export default function GeneratePaperPage() {
  const [meta, setMeta] = useState({
    semester: '',
    subject: '',
    subject_code: '',
    total_marks: 100,
  })
  const [modules, setModules] = useState([
    { module_number: 1, title: '', topics: '', num_questions: 2, marks: 20 },
  ])
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(false)
  const [syllabusFile, setSyllabusFile] = useState(null)
  const [referenceFile, setReferenceFile] = useState(null)
  const [referenceQpFile, setReferenceQpFile] = useState(null)

  const handleChange = (e) => {
    setMeta({ ...meta, [e.target.name]: e.target.value })
  }

  const uploadSyllabus = async () => {
    if (!syllabusFile) {
      throw new Error('Please select a syllabus file before generating the paper.')
    }
    if (!meta.semester || !meta.subject || !meta.subject_code) {
      throw new Error('Please fill Semester, Subject, and Subject Code before generating.')
    }

    const formData = new FormData()
    formData.append('semester', meta.semester)
    formData.append('subject', meta.subject)
    formData.append('subject_code', meta.subject_code)
    formData.append('file', syllabusFile)

    const res = await api.post('/files/upload-syllabus', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    return res.data.id
  }

  const uploadReferences = async () => {
    const referenceIds = []
    const refQpIds = []

    if (referenceFile) {
      const formData = new FormData()
      formData.append('title', referenceFile.name)
      formData.append('material_type', 'reference')
      formData.append('file', referenceFile)
      const res = await api.post('/files/upload-reference', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      referenceIds.push(res.data.id)
    }

    if (referenceQpFile) {
      const formData = new FormData()
      formData.append('title', referenceQpFile.name)
      formData.append('material_type', 'question_paper')
      formData.append('file', referenceQpFile)
      const res = await api.post('/files/upload-reference', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      refQpIds.push(res.data.id)
    }

    return { referenceIds, refQpIds }
  }

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const syllabusDocId = await uploadSyllabus()
      const { referenceIds, refQpIds } = await uploadReferences()

      const payload = {
        semester: meta.semester,
        subject: meta.subject,
        subject_code: meta.subject_code,
        total_marks: Number(meta.total_marks),
        modules,
        marks_distribution: null,
        syllabus_doc_id: syllabusDocId,
        reference_material_ids: referenceIds,
        reference_question_material_ids: refQpIds,
      }
      const res = await api.post('/papers/generate', payload)
      setPapers(res.data)
    } catch (err) {
      const msg = err?.response?.data?.detail || err.message || 'Failed to generate papers'
      alert(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h2>Generate Question Papers</h2>
      <div className="form-grid">
        <input
          name="semester"
          placeholder="Semester"
          value={meta.semester}
          onChange={handleChange}
        />
        <input
          name="subject"
          placeholder="Subject"
          value={meta.subject}
          onChange={handleChange}
        />
        <input
          name="subject_code"
          placeholder="Subject Code"
          value={meta.subject_code}
          onChange={handleChange}
        />
        <input
          type="number"
          name="total_marks"
          placeholder="Total Marks"
          value={meta.total_marks}
          onChange={handleChange}
        />
        <input
          type="file"
          onChange={(e) => setSyllabusFile(e.target.files[0])}
        />
        <input
          type="file"
          onChange={(e) => setReferenceFile(e.target.files[0])}
        />
        <input
          type="file"
          onChange={(e) => setReferenceQpFile(e.target.files[0])}
        />
      </div>

      <ModuleForm modules={modules} setModules={setModules} />

      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate 3 Sets'}
      </button>

      {papers.length > 0 && (
        <div className="papers-preview">
          <h3>Generated Papers</h3>
          {papers.map((p) => (
            <div key={p.id} className="paper-card">
              <h4>
                {p.subject} ({p.subject_code}) - Set {p.set_number}
              </h4>
              <p>Semester: {p.semester}</p>
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
      )}
    </div>
  )
}
