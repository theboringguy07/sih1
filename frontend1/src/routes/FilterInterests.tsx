import React, { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const INTERESTS = [
  'AI/ML', 'Web Development', 'Programming', 'Finance', 'Data Science', 'UI/UX Design', 'Product Management', 'Cybersecurity', 'Cloud Computing', 'DevOps', 'Marketing', 'Content Writing', 'Business Development', 'Blockchain', 'Mobile Apps', 'Computer Vision', 'NLP'
]

const FilterInterests: React.FC = () => {
  const navigate = useNavigate()
  const [selected, setSelected] = useState<string[]>([])
  const [touched, setTouched] = useState(false)

  const hasSelection = useMemo(() => selected.length > 0, [selected])

  const toggle = (item: string) => {
    setTouched(true)
    setSelected((prev) => (prev.includes(item) ? prev.filter((x) => x !== item) : [...prev, item]))
  }

  const handleContinue = () => {
    if (!hasSelection) return
    sessionStorage.setItem('interests', JSON.stringify(selected))
    navigate('/loading')
  }

  return (
    <div className="section">
      <h2>What are your interests?</h2>
      <div className="card center-card">
        <div className="interest-grid">
          {INTERESTS.map((it) => (
            <button
              key={it}
              className={`interest-btn ${selected.includes(it) ? 'selected' : ''}`}
              onClick={() => toggle(it)}
              type="button"
            >
              {it}
            </button>
          ))}
        </div>
        {!hasSelection && touched && (
          <div style={{ marginTop: 8 }} className="error">Please select at least one interest.</div>
        )}
        <div className="btn-row">
          <button className="btn-primary" onClick={handleContinue} disabled={!hasSelection}>
            Continue <span aria-hidden>→</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default FilterInterests


