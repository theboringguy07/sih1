import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Home from './components/Home';
import ProfileForm from './components/ProfileForm';
import RecommendationsPage from './components/RecommendationsPage';
import ResumeUpload from './components/ResumeUpload';
import LanguageProvider from './context/LanguageContext';

function App() {
  const [userProfile, setUserProfile] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  return (
    <LanguageProvider>
      <Router>
        <div className="App">
          <Header />
          <main className="main-content">
            <Routes>
              <Route 
                path="/" 
                element={<Home />} 
              />
              <Route 
                path="/profile" 
                element={
                  <ProfileForm 
                    userProfile={userProfile}
                    setUserProfile={setUserProfile}
                    setRecommendations={setRecommendations}
                  />
                } 
              />
              <Route 
                path="/upload-resume" 
                element={
                  <ResumeUpload 
                    setUserProfile={setUserProfile}
                    setRecommendations={setRecommendations}
                  />
                } 
              />
              <Route 
                path="/recommendations" 
                element={
                  <RecommendationsPage 
                    recommendations={recommendations}
                    userProfile={userProfile}
                  />
                } 
              />
            </Routes>
          </main>
        </div>
      </Router>
    </LanguageProvider>
  );
}

export default App;
