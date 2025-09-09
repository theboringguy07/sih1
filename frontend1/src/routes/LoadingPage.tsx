import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const LoadingPage: React.FC = () => {
  const navigate = useNavigate()

  useEffect(() => {
    const t = setTimeout(() => navigate('/results'), 1500)
    return () => clearTimeout(t)
  }, [navigate])

  return (
    <div className="loader-wrap">
      <div className="loader-text-top">Please Wait</div>
      <div className="loader" />
      <div className="loader-sub">Finding the best internships for you...</div>
    </div>
  )
}

export default LoadingPage


