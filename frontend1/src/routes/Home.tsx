import React from 'react'
import { useNavigate } from 'react-router-dom'

const Home: React.FC = () => {
  const navigate = useNavigate()
  return (
    <div>
      <section className="hero">
        <div>
          <h1>AI Based Internship Recommendation Engine</h1>
          <p>Find internships that truly match your skills, interests, and aspirations.</p>
          <button className="cta" onClick={() => navigate('/filter/about')}>
            Get My Recommendations
            <span aria-hidden>→</span>
          </button>
        </div>
        <div className="illust-grid below">
          <div className="illust yellow"><b>Smart Matching</b>Our AI analyzes your profile to find the perfect internship matches</div>
          <div className="illust blue"><b>Personalized Results</b>Get recommendations tailored specifically to your career goals</div>
        </div>
      </section>

      <section className="section">
        <div className="card center-card">
          <p>
            This portal uses an AI-powered recommendation system to suggest internships tailored for
            students and young professionals in India. Discover roles that fit your profile, interests, and
            location preferences.
          </p>
        </div>
      </section>
    </div>
  )
}

export default Home


