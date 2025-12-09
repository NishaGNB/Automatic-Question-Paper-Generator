export default function ModuleForm({ modules, setModules }) {
  const addModule = () => {
    setModules([
      ...modules,
      { module_number: modules.length + 1, title: '', topics: '', num_questions: 2, marks: 20 },
    ])
  }

  const updateModule = (index, field, value) => {
    const copy = [...modules]
    copy[index][field] = value
    setModules(copy)
  }

  const removeModule = (index) => {
    if (modules.length === 1) return
    const copy = modules.filter((_, i) => i !== index).map((m, i) => ({
      ...m,
      module_number: i + 1,
    }))
    setModules(copy)
  }

  return (
    <div className="module-form">
      <h3>Modules</h3>
      {modules.map((m, idx) => (
        <div key={idx} className="module-card">
          <h4>Module {m.module_number}</h4>
          <input
            placeholder="Module Title"
            value={m.title}
            onChange={(e) => updateModule(idx, 'title', e.target.value)}
          />
          <textarea
            placeholder="Topics (comma or line separated)"
            value={m.topics}
            onChange={(e) => updateModule(idx, 'topics', e.target.value)}
          />
          <div className="module-row">
            <input
              type="number"
              placeholder="Questions"
              value={m.num_questions}
              onChange={(e) => updateModule(idx, 'num_questions', Number(e.target.value))}
            />
            <input
              type="number"
              placeholder="Marks"
              value={m.marks}
              onChange={(e) => updateModule(idx, 'marks', Number(e.target.value))}
            />
          </div>
          {modules.length > 1 && (
            <button type="button" onClick={() => removeModule(idx)}>
              Remove Module
            </button>
          )}
        </div>
      ))}
      <button type="button" onClick={addModule}>
        Add Module
      </button>
    </div>
  )
}
