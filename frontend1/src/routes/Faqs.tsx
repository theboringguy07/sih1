import React, { useState } from 'react'

const faqs = [
  { q: 'What is the AI Internship Recommendation Engine?', a: 'A portal that suggests internships based on your profile and interests.' },
  { q: 'Is it free to use?', a: 'Yes, browsing and getting recommendations is free.' },
  { q: 'How are recommendations generated?', a: 'We use profile inputs and selected interests to match with available roles.' },
  { q: 'Do you store my data?', a: 'We store minimal information to personalize results; see Privacy on the About page.' },
]

const Faqs: React.FC = () => {
  const [openIdx, setOpenIdx] = useState<number | null>(0)
  return (
    <div className="section">
      <div className="card center-card" style={{ padding: 36 }}>
        <h1 style={{ marginTop: 0, textAlign: 'center', letterSpacing: 0.4 }}>FAQs</h1>
        <div>
          {faqs.map((f, idx) => (
            <div key={idx} style={{ borderTop: '1px solid var(--border)', padding: '12px 0' }}>
              <button
                onClick={() => setOpenIdx(idx === openIdx ? null : idx)}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text)',
                  fontWeight: 700,
                  padding: '8px 0',
                  cursor: 'pointer',
                }}
                aria-expanded={openIdx === idx}
              >
                {f.q}
              </button>
              {openIdx === idx && <div style={{ color: 'var(--muted)' }}>{f.a}</div>}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Faqs


