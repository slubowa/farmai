import React, { useState } from 'react';
import { Box, Button, TextField, Typography, CircularProgress, Paper } from '@mui/material';
import { askQuestion } from '../api/apiClient';
/**
 * A React component for a chat interface that allows users to interact with FarmAI.
 */
const Chat = () => {
  // State for storing the current question input by the user.
  const [question, setQuestion] = useState('');
  // State for storing the conversation history as an array of message objects.
  const [conversation, setConversation] = useState([]);
  // State to handle the loading state during API requests
  const [loading, setLoading] = useState(false);
/**
   * Handles the submission of the question to the backend.
   * Updates the conversation state with both the user's question and FarmAI's response.
   */
  const handleSubmit = async () => {
    setLoading(true);
    const res = await askQuestion(question); 
    setConversation(prev => [...prev, { type: 'Me', text: question }, { type: 'FarmAI', text: res.answer || res.error }]);
    setQuestion('');
    setLoading(false);
  };
/**
   * Handles the Enter key press to submit the question when pressed.
   */
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 2, position: 'fixed', bottom: 20, right: 20, maxWidth: 300, maxHeight: 600, width: '100%', display: 'flex', flexDirection: 'column', borderRadius: '5%' }}>
      <Typography variant="h6" gutterBottom component="div">
        Chat with FarmAI
      </Typography>
      <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2 }}>
        {conversation.map((entry, index) => (
          <Typography key={index} variant="body2" sx={{ color: entry.type === 'Me' ? 'blue' : 'green', mt: 1 }}>
            {entry.type}: {entry.text}
          </Typography>
        ))}
      </Box>
      <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 1 }} onKeyPress={handleKeyPress}>
        <TextField
          label="Your Question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          fullWidth
          variant="outlined"
          size="small"
        />
        <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading || !question.trim()}>
          {loading ? <CircularProgress size={24} /> : 'Ask'}
        </Button>
      </Box>
    </Paper>
  );
};

export default Chat;