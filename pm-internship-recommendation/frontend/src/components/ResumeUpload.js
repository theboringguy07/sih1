import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import apiService from '../services/apiService';

const ResumeUpload = ({ setUserProfile, setRecommendations }) => {
  const { translate } = useLanguage();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleFile = async (file) => {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a PDF, DOC, or DOCX file.');
      return;
    }

    if (file.size > maxSize) {
      setError('File size should be less than 5MB.');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');
    setProgress(0);

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev < 90) return prev + 10;
          return prev;
        });
      }, 200);

      // Parse resume
      const parseResult = await apiService.parseResume(file);
      clearInterval(progressInterval);
      setProgress(100);

      if (parseResult.success) {
        const profileData = parseResult.data;
        setUserProfile(profileData);
        setSuccess('Resume parsed successfully!');

        // Auto-get recommendations if we have enough data
        if (profileData.education && profileData.skills && profileData.skills.length > 0) {
          setTimeout(async () => {
            try {
              const recommendations = await apiService.getRecommendations(profileData);
              setRecommendations(recommendations);
              navigate('/recommendations');
            } catch (err) {
              // Navigate to profile form if recommendations fail
              navigate('/profile');
            }
          }, 1500);
        } else {
          // Navigate to profile form to complete the profile
          setTimeout(() => {
            navigate('/profile');
          }, 1500);
        }
      } else {
        throw new Error(parseResult.message || 'Failed to parse resume');
      }

    } catch (err) {
      setError(err.message || 'Failed to parse resume. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="upload-container">
      <div className="form-container">
        <h2 className="form-title">{translate('uploadResume')}</h2>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        {success && (
          <div className="success-message">
            {success}
          </div>
        )}

        {uploading && (
          <div className="upload-progress">
            <div className="loading">
              <div className="spinner"></div>
              {translate('processingResume')}
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div style={{ textAlign: 'center', fontSize: '14px', color: '#666' }}>
              {progress}%
            </div>
          </div>
        )}

        {!uploading && (
          <div
            className={`upload-area ${dragOver ? 'dragover' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={openFileDialog}
          >
            <div className="upload-icon">📄</div>
            <div className="upload-text">
              {translate('dragDropResume')}
            </div>
            <div className="upload-subtext">
              {translate('supportedFormats')}
            </div>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          className="file-input"
          accept=".pdf,.doc,.docx"
          onChange={handleFileSelect}
        />

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <p style={{ color: 'white', fontSize: '14px', marginBottom: '10px' }}>
            Or fill out the profile form manually
          </p>
          <button
            onClick={() => navigate('/profile')}
            className="btn btn-secondary"
            disabled={uploading}
          >
            📝 {translate('fillProfileForm')}
          </button>
        </div>

        <div style={{ marginTop: '30px', color: 'rgba(255, 255, 255, 0.8)', fontSize: '14px' }}>
          <h4>What we'll extract from your resume:</h4>
          <ul style={{ textAlign: 'left', marginTop: '10px' }}>
            <li>Education details</li>
            <li>Skills and technologies</li>
            <li>Location information</li>
            <li>Contact information</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ResumeUpload;
