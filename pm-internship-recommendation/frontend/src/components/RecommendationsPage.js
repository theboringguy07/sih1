import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const RecommendationsPage = ({ recommendations, userProfile }) => {
  const { translate } = useLanguage();

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="recommendations-container">
        <div className="form-container">
          <h2 className="form-title">{translate('recommendations')}</h2>
          <p style={{ textAlign: 'center', color: '#666', marginBottom: '20px' }}>
            {translate('noRecommendations')}
          </p>
          <div style={{ textAlign: 'center' }}>
            <Link to="/profile" className="btn btn-primary">
              {translate('tryAgain')}
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const handleApply = (internship) => {
    // In a real application, this would redirect to the application page
    alert(`Applying for ${internship.title} at ${internship.company}`);
  };

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h1>🎯 {translate('recommendations')}</h1>
        <p>
          Based on your profile, here are the top {recommendations.length} internships for you:
        </p>
        {userProfile && (
          <div style={{ marginTop: '15px', fontSize: '14px', opacity: 0.9 }}>
            <span>📚 {userProfile.education}</span>
            {userProfile.location && <span> • 📍 {userProfile.location}</span>}
            {userProfile.skills && userProfile.skills.length > 0 && (
              <span> • 🔧 {userProfile.skills.slice(0, 3).join(', ')}</span>
            )}
          </div>
        )}
      </div>

      <div className="recommendations-grid">
        {recommendations.map((internship, index) => (
          <div key={internship.id || index} className="recommendation-card">
            <div className="match-score">
              {internship.match_score}% {translate('matchScore')}
            </div>
            
            <h3 className="card-title">{internship.title}</h3>
            <p className="card-company">{internship.company}</p>
            
            <div className="card-details">
              <div className="detail-item">
                <span className="detail-label">{translate('location')}:</span> {internship.location}
              </div>
              <div className="detail-item">
                <span className="detail-label">{translate('duration')}:</span> {internship.duration}
              </div>
              <div className="detail-item">
                <span className="detail-label">{translate('stipend')}:</span> {internship.stipend}
              </div>
              <div className="detail-item">
                <span className="detail-label">Sector:</span> {internship.sector}
              </div>
            </div>
            
            <p className="card-description">
              {internship.description}
            </p>
            
            {internship.match_reasons && internship.match_reasons.length > 0 && (
              <div className="match-reasons">
                <h4>{translate('whyThisMatches')}:</h4>
                <ul>
                  {internship.match_reasons.map((reason, reasonIndex) => (
                    <li key={reasonIndex}>{reason}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {internship.requirements && (
              <div style={{ marginBottom: '15px' }}>
                <h4 style={{ fontSize: '14px', marginBottom: '8px', color: '#333' }}>
                  {translate('requirements')}:
                </h4>
                <div style={{ fontSize: '13px', color: '#666' }}>
                  <p><strong>{translate('education')}:</strong> {internship.requirements.education}</p>
                  {internship.requirements.skills && (
                    <p><strong>{translate('skills')}:</strong> {internship.requirements.skills.join(', ')}</p>
                  )}
                </div>
              </div>
            )}
            
            <button
              onClick={() => handleApply(internship)}
              className="btn btn-success"
              style={{ width: '100%' }}
            >
              {translate('applyNow')} 🚀
            </button>
          </div>
        ))}
      </div>

      <div style={{ textAlign: 'center', marginTop: '40px' }}>
        <div style={{ 
          background: 'rgba(255, 255, 255, 0.1)', 
          padding: '20px', 
          borderRadius: '15px',
          marginBottom: '20px'
        }}>
          <h3 style={{ color: 'white', marginBottom: '15px' }}>
            Want to update your profile?
          </h3>
          <div style={{ display: 'flex', gap: '15px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/profile" className="btn btn-secondary">
              📝 Edit Profile
            </Link>
            <Link to="/upload-resume" className="btn btn-secondary">
              📄 Upload New Resume
            </Link>
            <Link to="/" className="btn btn-info">
              🏠 Start Over
            </Link>
          </div>
        </div>
        
        <div style={{ color: 'rgba(255, 255, 255, 0.8)', fontSize: '14px' }}>
          <p>💡 Tip: Update your skills and interests regularly to get better recommendations</p>
          <p>📞 Need help? Contact PM Internship Support</p>
        </div>
      </div>
    </div>
  );
};

export default RecommendationsPage;
