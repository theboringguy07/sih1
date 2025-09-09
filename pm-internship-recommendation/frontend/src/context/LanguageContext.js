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
    },
    te: {
      welcome: 'స్వాగతం',
      internship: 'ఇంటర్న్‌షిప్',
      recommendations: 'సిఫార్సులు',
      skills: 'నైపుణ్యాలు',
      education: 'విద్య',
      location: 'స్థలం',
      profile: 'ప్రొఫైల్',
      uploadResume: 'రెజ్యూమే అప్‌లోడ్ చేయండి',
      getRecommendations: 'సిఫార్సులు పొందండి',
      submit: 'సమర్పించండి',
      next: 'తదుపరి',
      back: 'వెనుకకు',
      search: 'వెతకండి',
      applyNow: 'ఇప్పుడే దరఖాస్తు చేయండి',
      duration: 'వ్యవధి',
      stipend: 'జీతం',
      company: 'కంపెనీ',
      description: 'వివరణ',
      requirements: 'అవసరాలు',
      name: 'పేరు',
      email: 'ఇమెయిల్',
      phone: 'ఫోన్',
      interests: 'ఆసక్తులు',
      matchScore: 'మ్యాచ్ స్కోర్',
      whyThisMatches: 'ఇది ఎందుకు సరిపోతుంది',
      createProfile: 'ప్రొఫైల్ సృష్టించండి',
      fillProfileForm: 'ప్రొఫైల్ ఫారం నింపండి',
      pmInternshipScheme: 'PM ఇంటర్న్‌షిప్ పథకం',
      findYourPerfectInternship: 'మీ పరిపూర్ణ ఇంటర్న్‌షిప్‌ను కనుగొనండి',
      aiPoweredRecommendations: 'మీ నైపుణ్యాలు మరియు ఆసక్తులకు అనుగుణంగా AI-ఆధారిత సిఫార్సులను పొందండి',
      chooseHowToStart: 'మీరు ఎలా ప్రారంభించాలనుకుంటున్నారో ఎంచుకోండి:',
      manuallyEnterDetails: 'మీ వివరాలను మాన్యువల్‌గా నమోదు చేయండి',
      uploadYourResume: 'త్వరిత సెటప్ కోసం మీ రెజ్యూమేను అప్‌లోడ్ చేయండి',
      loading: 'లోడ్ అవుతోంది...',
      processingResume: 'మీ రెజ్యూమే ప్రాసెస్ చేయబడుతోంది...',
      gettingRecommendations: 'మీ సిఫార్సులు పొందబడుతున్నాయి...',
      error: 'లోపం',
      success: 'విజయం',
      noRecommendations: 'ఎటువంటి సిఫార్సులు కనుగొనబడలేదు. దయచేసి మీ ప్రొఫైల్‌ను నవీకరించండి.',
      tryAgain: 'మళ్లీ ప్రయత్నించండి',
      dragDropResume: 'మీ రెజ్యూమేను ఇక్కడ డ్రాగ్ మరియు డ్రాప్ చేయండి లేదా ఎంచుకోవడానికి క్లిక్ చేయండి',
      supportedFormats: 'మద్దతు ఉన్న ఫార్మాట్‌లు: PDF, DOC, DOCX'
    },
    ta: {
      welcome: 'வரவேற்கிறோம்',
      internship: 'பயிற்சி',
      recommendations: 'பரிந்துரைகள்',
      skills: 'திறமைகள்',
      education: 'கல்வி',
      location: 'இடம்',
      profile: 'சுயவிவரம்',
      uploadResume: 'விவரக்குறிப்பை பதிவேற்றவும்',
      getRecommendations: 'பரிந்துரைகளைப் பெறுங்கள்',
      submit: 'சமர்ப்பிக்கவும்',
      next: 'அடுத்தது',
      back: 'திரும்பு',
      search: 'தேடுங்கள்',
      applyNow: 'இப்போதே விண்ணப்பிக்கவும்',
      duration: 'காலம்',
      stipend: 'உதவித்தொகை',
      company: 'நிறுவனம்',
      description: 'விளக்கம்',
      requirements: 'தேவைகள்',
      name: 'பெயர்',
      email: 'மின்னஞ்சல்',
      phone: 'தொலைபேசி',
      interests: 'ஆர்வங்கள்',
      matchScore: 'பொருத்த மதிப்பெண்',
      whyThisMatches: 'இது ஏன் பொருந்துகிறது',
      createProfile: 'சுயவிவரம் உருவாக்கவும்',
      fillProfileForm: 'சுயவிவர படிவத்தை நிரப்பவும்',
      pmInternshipScheme: 'PM பயிற்சி திட்டம்',
      findYourPerfectInternship: 'உங்கள் சரியான பயிற்சியைக் கண்டறியுங்கள்',
      aiPoweredRecommendations: 'உங்கள் திறமைகள் மற்றும் ஆர்வங்களுக்கு ஏற்ப AI-இயங்கும் பரிந்துரைகளைப் பெறுங்கள்',
      chooseHowToStart: 'எப்படி தொடங்க விரும்புகிறீர்கள் என்பதைத் தேர்வுசெய்யுங்கள்:',
      manuallyEnterDetails: 'உங்கள் விவரங்களை கைமுறையாக உள்ளிடுங்கள்',
      uploadYourResume: 'விரைவு அமைப்புக்கு உங்கள் விவரக்குறிப்பை பதிவேற்றவும்',
      loading: 'ஏற்றுகிறது...',
      processingResume: 'உங்கள் விவரக்குறிப்பு செயலாக்கப்படுகிறது...',
      gettingRecommendations: 'உங்கள் பரிந்துரைகள் பெறப்படுகின்றன...',
      error: 'பிழை',
      success: 'வெற்றி',
      noRecommendations: 'பரிந்துரைகள் எதுவும் கிடைக்கவில்லை. தயவுசெய்து உங்கள் சுயவிவரத்தை புதுப்பிக்கவும்.',
      tryAgain: 'மீண்டும் முயற்சிக்கவும்',
      dragDropResume: 'உங்கள் விவரக்குறிப்பை இங்கே இழுத்து விடவும் அல்லது தேர்வுசெய்ய கிளிக் செய்யவும்',
      supportedFormats: 'ஆதரிக்கப்படும் வடிவங்கள்: PDF, DOC, DOCX'
    },
    bn: {
      welcome: 'স্বাগতম',
      internship: 'ইন্টার্নশিপ',
      recommendations: 'সুপারিশ',
      skills: 'দক্ষতা',
      education: 'শিক্ষা',
      location: 'অবস্থান',
      profile: 'প্রোফাইল',
      uploadResume: 'জীবনবৃত্তান্ত আপলোড করুন',
      getRecommendations: 'সুপারিশ পান',
      submit: 'জমা দিন',
      next: 'পরবর্তী',
      back: 'পিছনে',
      search: 'খুঁজুন',
      applyNow: 'এখনই আবেদন করুন',
      duration: 'সময়কাল',
      stipend: 'উপবৃত্তি',
      company: 'কোম্পানি',
      description: 'বর্ণনা',
      requirements: 'প্রয়োজনীয়তা',
      name: 'নাম',
      email: 'ইমেইল',
      phone: 'ফোন',
      interests: 'আগ্রহ',
      matchScore: 'ম্যাচ স্কোর',
      whyThisMatches: 'এটি কেন মিলে',
      createProfile: 'প্রোফাইল তৈরি করুন',
      fillProfileForm: 'প্রোফাইল ফর্ম পূরণ করুন',
      pmInternshipScheme: 'PM ইন্টার্নশিপ প্রকল্প',
      findYourPerfectInternship: 'আপনার পারফেক্ট ইন্টার্নশিপ খুঁজে নিন',
      aiPoweredRecommendations: 'আপনার দক্ষতা ও আগ্রহের সাথে মানানসই AI-চালিত সুপারিশ পান',
      chooseHowToStart: 'আপনি কিভাবে শুরু করতে চান তা বেছে নিন:',
      manuallyEnterDetails: 'আপনার বিবরণ ম্যানুয়ালি প্রবেশ করান',
      uploadYourResume: 'দ্রুত সেটআপের জন্য আপনার জীবনবৃত্তান্ত আপলোড করুন',
      loading: 'লোড হচ্ছে...',
      processingResume: 'আপনার জীবনবৃত্তান্ত প্রক্রিয়া করা হচ্ছে...',
      gettingRecommendations: 'আপনার সুপারিশ পাওয়া হচ্ছে...',
      error: 'ত্রুটি',
      success: 'সফলতা',
      noRecommendations: 'কোন সুপারিশ পাওয়া যায়নি। দয়া করে আপনার প্রোফাইল আপডেট করুন।',
      tryAgain: 'আবার চেষ্টা করুন',
      dragDropResume: 'আপনার জীবনবৃত্তান্ত এখানে ড্র্যাগ ও ড্রপ করুন বা নির্বাচন করতে ক্লিক করুন',
      supportedFormats: 'সমর্থিত ফরম্যাট: PDF, DOC, DOCX'
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
