import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import apiService from '../services/apiService';

const ProfileForm = ({ userProfile, setUserProfile, setRecommendations }) => {
  const { translate } = useLanguage();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    name: userProfile?.name || '',
    email: userProfile?.email || '',
    phone: userProfile?.phone || '',
    education: userProfile?.education || '',
    location: userProfile?.location || '',
    skills: userProfile?.skills || [],
    interests: userProfile?.interests || []
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [newSkill, setNewSkill] = useState('');
  const [newInterest, setNewInterest] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const addSkill = () => {
    if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
      setFormData(prev => ({
        ...prev,
        skills: [...prev.skills, newSkill.trim()]
      }));
      setNewSkill('');
    }
  };

  const removeSkill = (skillToRemove) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.filter(skill => skill !== skillToRemove)
    }));
  };

  const addInterest = () => {
    if (newInterest.trim() && !formData.interests.includes(newInterest.trim())) {
      setFormData(prev => ({
        ...prev,
        interests: [...prev.interests, newInterest.trim()]
      }));
      setNewInterest('');
    }
  };

  const removeInterest = (interestToRemove) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.filter(interest => interest !== interestToRemove)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Save profile
      setUserProfile(formData);
      
      // Get recommendations
      const recommendations = await apiService.getRecommendations(formData);
      setRecommendations(recommendations);
      
      // Navigate to recommendations page
      navigate('/recommendations');
    } catch (err) {
      setError(err.message || 'Failed to get recommendations');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2 className="form-title">{translate('createProfile')}</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>{translate('name')}</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label>{translate('email')}</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label>{translate('phone')}</label>
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>{translate('education')}</label>
          <select
            name="education"
            value={formData.education}
            onChange={handleInputChange}
            className="form-select"
            required
          >
            <option value="">Select your education</option>
            <option value="10th">10th Standard</option>
            <option value="12th">12th Standard</option>
            <option value="Diploma">Diploma</option>
            <option value="B.Tech">B.Tech</option>
            <option value="B.Sc">B.Sc</option>
            <option value="B.Com">B.Com</option>
            <option value="B.A">B.A</option>
            <option value="BBA">BBA</option>
            <option value="M.Tech">M.Tech</option>
            <option value="M.Sc">M.Sc</option>
            <option value="MBA">MBA</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label>{translate('location')}</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            className="form-input"
            placeholder="City, State"
            required
          />
        </div>

        <div className="form-group">
          <label>{translate('skills')}</label>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              className="form-input"
              placeholder="Add a skill"
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
            />
            <button
              type="button"
              onClick={addSkill}
              className="btn btn-secondary"
              style={{ minWidth: '80px' }}
            >
              Add
            </button>
          </div>
          <div className="skills-container">
            {formData.skills.map((skill, index) => (
              <div key={index} className="skill-tag">
                {skill}
                <button
                  type="button"
                  onClick={() => removeSkill(skill)}
                  className="skill-remove"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>{translate('interests')}</label>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
            <input
              type="text"
              value={newInterest}
              onChange={(e) => setNewInterest(e.target.value)}
              className="form-input"
              placeholder="Add an interest"
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addInterest())}
            />
            <button
              type="button"
              onClick={addInterest}
              className="btn btn-secondary"
              style={{ minWidth: '80px' }}
            >
              Add
            </button>
          </div>
          <div className="skills-container">
            {formData.interests.map((interest, index) => (
              <div key={index} className="skill-tag">
                {interest}
                <button
                  type="button"
                  onClick={() => removeInterest(interest)}
                  className="skill-remove"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary"
          style={{ width: '100%', marginTop: '20px' }}
        >
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              {translate('gettingRecommendations')}
            </div>
          ) : (
            translate('getRecommendations')
          )}
        </button>
      </form>
    </div>
  );
};

export default ProfileForm;
