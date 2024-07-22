import React, { useState } from 'react';
import { Box, Button, TextField, Typography, CircularProgress, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { getCreditScore } from '../api/apiClient';

const CreditScoring = () => {
  const [incomeMonth1, setIncomeMonth1] = useState('');
  const [incomeMonth2, setIncomeMonth2] = useState('');
  const [incomeMonth3, setIncomeMonth3] = useState('');
  const [expenseMonth1, setExpenseMonth1] = useState('');
  const [expenseMonth2, setExpenseMonth2] = useState('');
  const [expenseMonth3, setExpenseMonth3] = useState('');
  const [yieldMonth1, setYieldMonth1] = useState('');
  const [yieldMonth2, setYieldMonth2] = useState('');
  const [yieldMonth3, setYieldMonth3] = useState('');
  const [communityEngagement, setCommunityEngagement] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateVariances = (values) => {
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;
    return { mean, variance, stability: Math.sqrt(variance) / mean };
  };

  const mapCommunityEngagement = (response) => {
    const communityEngagementMap = {
      "Never": 0,
      "Rarely": 2,
      "Sometimes": 4,
      "Often": 8,
      "Very frequently": 10
    };
    return communityEngagementMap[response] || 0; // Default to 0 if response not in map
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const incomeValues = [parseFloat(incomeMonth1), parseFloat(incomeMonth2), parseFloat(incomeMonth3)];
      const expenseValues = [parseFloat(expenseMonth1), parseFloat(expenseMonth2), parseFloat(expenseMonth3)];
      const yieldValues = [parseFloat(yieldMonth1), parseFloat(yieldMonth2), parseFloat(yieldMonth3)];

      const incomeStats = calculateVariances(incomeValues);
      const expenseStats = calculateVariances(expenseValues);
      const yieldConsistency = calculateVariances(yieldValues).variance;
      const communityEngagementValue = mapCommunityEngagement(communityEngagement);

      const data = [{
        income_stability: incomeStats.stability,
        income_mean: incomeStats.mean,
        expense_stability: expenseStats.stability,
        expense_mean: expenseStats.mean,
        yield_consistency: yieldConsistency,
        community_engagement: communityEngagementValue
      }];

      const response = await getCreditScore(data);
      setResult(response);
    } catch (error) {
      console.error(error);
      setResult({ error: 'Failed to get credit score' });
    }
    setLoading(false);
  };
  
  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Credit Scoring
      </Typography>
      <TextField
        label="Income Month 1"
        value={incomeMonth1}
        onChange={(e) => setIncomeMonth1(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Income Month 2"
        value={incomeMonth2}
        onChange={(e) => setIncomeMonth2(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Income Month 3"
        value={incomeMonth3}
        onChange={(e) => setIncomeMonth3(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Expenses Month 1"
        value={expenseMonth1}
        onChange={(e) => setExpenseMonth1(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Expenses Month 2"
        value={expenseMonth2}
        onChange={(e) => setExpenseMonth2(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Expenses Month 3"
        value={expenseMonth3}
        onChange={(e) => setExpenseMonth3(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Yield Month 1"
        value={yieldMonth1}
        onChange={(e) => setYieldMonth1(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Yield Month 2"
        value={yieldMonth2}
        onChange={(e) => setYieldMonth2(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Yield Month 3"
        value={yieldMonth3}
        onChange={(e) => setYieldMonth3(e.target.value)}
        fullWidth
        margin="normal"
      />
      <FormControl fullWidth margin="normal">
        <InputLabel>Community Engagement</InputLabel>
        <Select
          value={communityEngagement}
          onChange={(e) => setCommunityEngagement(e.target.value)}
        >
          <MenuItem value="Never">Never</MenuItem>
          <MenuItem value="Rarely">Rarely</MenuItem>
          <MenuItem value="Sometimes">Sometimes</MenuItem>
          <MenuItem value="Often">Often</MenuItem>
          <MenuItem value="Very frequently">Very frequently</MenuItem>
        </Select>
      </FormControl>
      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : 'Get Credit Score'}
      </Button>
      {result && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">Credit Score Result:</Typography>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </Box>
      )}
    </Box>
  );
};

export default CreditScoring;