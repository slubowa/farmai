import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5001/';

export const getFertilizerRecommendation = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/fertilizer_recommendation`, data);
    return response.data;
};

export const getCreditScore = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/predict`, data);
    console.log(response.data)
    return response.data;
};

export const askQuestion = async (question) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, { question });
      console.log(response.data.answer);
      return response.data;

    } catch (error) {
      console.error('Error asking question:', error);
      return { error: 'Failed to get response' };
    }
  };