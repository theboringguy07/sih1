import React, { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const FilterAbout: React.FC = () => {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [education, setEducation] = useState('')
  const [field, setField] = useState('')
  const [location, setLocation] = useState('')
  const [touched, setTouched] = useState<Record<string, boolean>>({})

  const allValid = useMemo(() => name.trim() && education && field.trim() && location.trim(), [name, education, field, location])

  const handleContinue = () => {
    if (!allValid) return
    sessionStorage.setItem('profile', JSON.stringify({ name, education, field, location }))
    navigate('/filter/interests')
  }

  const onBlur = (key: string) => setTouched((t) => ({ ...t, [key]: true }))

  return (
    <div className="section">
      <h2>Tell us about yourself.</h2>
      <div className="card center-card">
        <div className="field">
          <label className="label" htmlFor="name">Name</label>
          <input id="name" className="input" placeholder="Enter your name" value={name} onChange={(e) => setName(e.target.value)} onBlur={() => onBlur('name')} />
          {!name.trim() && touched.name && <span className="error">Please fill this field</span>}
        </div>
        <div className="field">
          <label className="label" htmlFor="education">Education Level</label>
          <select id="education" className="select" value={education} onChange={(e) => setEducation(e.target.value)} onBlur={() => onBlur('education')}>
            <option value="" disabled>Choose your education level</option>
            <option value="High School">High School</option>
            <option value="Diploma">Diploma</option>
            <option value="Undergraduate">Undergraduate</option>
            <option value="Postgraduate">Postgraduate</option>
            <option value="PhD">PhD</option>
          </select>
          {!education && touched.education && <span className="error">Please fill this field</span>}
        </div>
        <div className="field">
          <label className="label" htmlFor="field">Field Of Study</label>
          <input id="field" className="input" placeholder="Enter your field of study" value={field} onChange={(e) => setField(e.target.value)} onBlur={() => onBlur('field')} />
          {!field.trim() && touched.field && <span className="error">Please fill this field</span>}
        </div>
        <div className="field">
          <label className="label" htmlFor="location">Location</label>
          <input id="location" className="input" placeholder="Enter your location" value={location} onChange={(e) => setLocation(e.target.value)} onBlur={() => onBlur('location')} />
          {!location.trim() && touched.location && <span className="error">Please fill this field</span>}
        </div>
        <div className="btn-row">
          <button className="btn-primary" onClick={handleContinue} disabled={!allValid}>
            Continue <span aria-hidden>→</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default FilterAbout


