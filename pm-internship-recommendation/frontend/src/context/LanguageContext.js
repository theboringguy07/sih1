import React, { createContext, useContext, useState } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  
  const supportedLanguages = {
    en: 'English',
    hi: 'हिंदी (Hindi)',
    te: 'తెలుగు (Telugu)',
    ta: 'தமிழ் (Tamil)',
    bn: 'বাংলা (Bengali)'
  };

  // Basic translations for common UI elements
  const translations = {
    en: {
      welcome: 'Welcome',
      internship: 'Internship',
      recommendations: 'Recommendations',
      skills: 'Skills',
      education: 'Education',
      location: 'Location',
      profile: 'Profile',
      uploadResume: 'Upload Resume',
      getRecommendations: 'Get Recommendations',
      submit: 'Submit',
      next: 'Next',
      back: 'Back',
      search: 'Search',
      applyNow: 'Apply Now',
      duration: 'Duration',
      stipend: 'Stipend',
      company: 'Company',
      description: 'Description',
      requirements: 'Requirements',
      name: 'Name',
      email: 'Email',
      phone: 'Phone',
      interests: 'Interests',
      matchScore: 'Match Score',
      whyThisMatches: 'Why this matches',
      createProfile: 'Create Profile',
      fillProfileForm: 'Fill Profile Form',
      pmInternshipScheme: 'PM Internship Scheme',
      findYourPerfectInternship: 'Find Your Perfect Internship',
      aiPoweredRecommendations: 'Get AI-powered recommendations tailored to your skills and interests',
      chooseHowToStart: 'Choose how you\'d like to start:',
      manuallyEnterDetails: 'Manually enter your details',
      uploadYourResume: 'Upload your resume for quick setup',
      loading: 'Loading...',
      processingResume: 'Processing your resume...',
      gettingRecommendations: 'Getting your recommendations...',
      error: 'Error',
      success: 'Success',
      noRecommendations: 'No recommendations found. Please update your profile.',
      tryAgain: 'Try Again',
      dragDropResume: 'Drag and drop your resume here or click to select',
      supportedFormats: 'Supported formats: PDF, DOC, DOCX'
    },
    hi: {
      welcome: 'स्वागत',
      internship: 'प्रशिक्षण',
      recommendations: 'सिफारिशें',
      skills: 'कौशल',
      education: 'शिक्षा',
      location: 'स्थान',
      profile: 'प्रोफ़ाइल',
      uploadResume: 'रिज्यूमे अपलोड करें',
      getRecommendations: 'सिफारिशें प्राप्त करें',
      submit: 'जमा करें',
      next: 'अगला',
      back: 'वापस',
      search: 'खोजें',
      applyNow: 'अभी आवेदन करें',
      duration: 'अवधि',
      stipend: 'वेतन',
      company: 'कंपनी',
      description: 'विवरण',
      requirements: 'आवश्यकताएं',
      name: 'नाम',
      email: 'ईमेल',
      phone: 'फोन',
      interests: 'रुचियां',
      matchScore: 'मैच स्कोर',
      whyThisMatches: 'यह क्यों मैच करता है',
      createProfile: 'प्रोफ़ाइल बनाएं',
      fillProfileForm: 'प्रोफ़ाइल फॉर्म भरें',
      pmInternshipScheme: 'पीएम इंटर्नशिप योजना',
      findYourPerfectInternship: 'अपना परफेक्ट इंटर्नशिप खोजें',
      aiPoweredRecommendations: 'अपने कौशल और रुचियों के अनुरूप AI-संचालित सिफारिशें प्राप्त करें',
      chooseHowToStart: 'चुनें कि आप कैसे शुरू करना चाहते हैं:',
      manuallyEnterDetails: 'अपनी जानकारी मैन्युअल रूप से दर्ज करें',
      uploadYourResume: 'त्वरित सेटअप के लिए अपना रिज्यूमे अपलोड करें',
      loading: 'लोड हो रहा है...',
      processingResume: 'आपका रिज्यूमे प्रोसेस हो रहा है...',
      gettingRecommendations: 'आपकी सिफारिशें ली जा रही हैं...',
      error: 'त्रुटि',
      success: 'सफलता',
      noRecommendations: 'कोई सिफारिश नहीं मिली। कृपया अपनी प्रोफ़ाइल अपडेट करें।',
      tryAgain: 'पुनः प्रयास करें',
      dragDropResume: 'अपना रिज्यूमे यहां ड्रैग और ड्रॉप करें या चुनने के लिए क्लिक करें',
      supportedFormats: 'समर्थित प्रारूप: PDF, DOC, DOCX'
    }
  };

  const translate = (key) => {
    return translations[currentLanguage]?.[key] || translations.en[key] || key;
  };

  const changeLanguage = (language) => {
    if (supportedLanguages[language]) {
      setCurrentLanguage(language);
    }
  };

  const value = {
    currentLanguage,
    supportedLanguages,
    translate,
    changeLanguage
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export default LanguageProvider;
