import axios from 'axios';

/** Base URL for the backend API */
const API_BASE_URL = 'http://127.0.0.1:5001/';
/**
 * Fetches fertilizer recommendation from the backend.
 * This function sends a data object containing necessary parameters to the backend API.
 * @param {Object} data - The data to send in the request body.
 * @returns {Promise<Object>} - The fertilizer recommendation from the backend.
 */
export const getFertilizerRecommendation = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/fertilizer_recommendation`, data);
    return response.data;
};
/**
 * Fetches credit score predictions.
 * Sends user data to the backend to receive a credit score prediction.
 * @param {Object} data - The data to send in the request body.
 * @returns {Promise<Object>} - The credit score prediction from the backend.
 */
export const getCreditScore = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/predict`, data);
    console.log(response.data)
    return response.data;
};
/**
 * Sends a question to the backend and receives an answer.
 * Handles interactions with a chatbot or AI assistant.
 * @param {string} question - The question to ask.
 * @returns {Promise<Object>} - The response from the backend containing the answer.
 */
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