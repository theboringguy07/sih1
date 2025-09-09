import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const Header = () => {
  const { currentLanguage, supportedLanguages, translate, changeLanguage } = useLanguage();

  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          {translate('pmInternshipScheme')}
        </Link>
        <div className="language-selector">
          <select 
            value={currentLanguage} 
            onChange={(e) => changeLanguage(e.target.value)}
          >
            {Object.entries(supportedLanguages).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
};

export default Header;
