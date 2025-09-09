import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiService = {
  // Get internship recommendations
  async getRecommendations(profileData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/recommend`, profileData);
      return response.data.recommendations;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get recommendations');
    }
  },

  // Parse resume
  async parseResume(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE_URL}/parse-resume`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to parse resume');
    }
  },

  // Get all internships
  async getAllInternships() {
    try {
      const response = await axios.get(`${API_BASE_URL}/internships`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch internships');
    }
  },

  // Translate text
  async translateText(text, targetLanguage) {
    try {
      const response = await axios.post(`${API_BASE_URL}/translate`, {
        text,
        target_language: targetLanguage
      });
      return response.data.translated_text;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to translate text');
    }
  },

  // Create/update user profile
  async saveProfile(profileData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/profile`, profileData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to save profile');
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      throw new Error('API service is not available');
    }
  },

  // Get supported languages
  async getSupportedLanguages() {
    try {
      const response = await axios.get(`${API_BASE_URL}/languages`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch supported languages');
    }
  },

  // Detect language of text
  async detectLanguage(text) {
    try {
      const response = await axios.post(`${API_BASE_URL}/detect-language`, {
        text
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to detect language');
    }
  },

  // Get recommendations with language preference
  async getMultilingualRecommendations(profileData, targetLanguage = 'en') {
    try {
      const response = await axios.post(`${API_BASE_URL}/recommend`, {
        ...profileData,
        target_language: targetLanguage
      });
      return response.data.recommendations;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get multilingual recommendations');
    }
  },

  // Process multilingual query
  async processMultilingualQuery(queryText) {
    try {
      const response = await axios.post(`${API_BASE_URL}/process-query`, {
        query: queryText
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to process multilingual query');
    }
  },

  // Get translation mode and capabilities
  async getTranslationCapabilities() {
    try {
      const response = await axios.get(`${API_BASE_URL}/translation-mode`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get translation capabilities');
    }
  }
};

export default apiService;
