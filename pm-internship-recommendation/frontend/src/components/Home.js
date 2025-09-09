import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const Home = () => {
  const { translate } = useLanguage();

  return (
    <div className="home-container">
      <h1 className="home-title">
        {translate('findYourPerfectInternship')}
      </h1>
      <p className="home-subtitle">
        {translate('aiPoweredRecommendations')}
      </p>
      
      <div className="home-options">
        <h3 style={{ color: 'white', marginBottom: '20px' }}>
          {translate('chooseHowToStart')}
        </h3>
        
        <Link to="/profile" className="btn btn-primary">
          📝 {translate('fillProfileForm')}
        </Link>
        
        <Link to="/upload-resume" className="btn btn-secondary">
          📄 {translate('uploadResume')}
        </Link>
      </div>
      
      <div style={{ marginTop: '40px', color: 'rgba(255, 255, 255, 0.8)', fontSize: '14px' }}>
        <p>✅ {translate('aiPoweredRecommendations')}</p>
        <p>🎯 Top 3-5 personalized suggestions</p>
        <p>📱 Mobile-friendly interface</p>
        <p>🌐 Regional language support</p>
      </div>
    </div>
  );
};

export default Home;
