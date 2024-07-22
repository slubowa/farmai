import React, { useState } from 'react';
import { Box, Button, TextField, Typography, CircularProgress } from '@mui/material';
import { getFertilizerRecommendation } from '../api/apiClient';

const FertilizerRecommendation = () => {
  const [areaName, setAreaName] = useState('');
  const [cropType, setCropType] = useState('');
  const [farmSize, setFarmSize] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await getFertilizerRecommendation({
        area_name: areaName,
        crop_type: cropType,
        farm_size_acres: farmSize,
        
      });
      setResult(response);
    } catch (error) {
      console.error(error);
      setResult({ error: 'Failed to get fertilizer recommendation' });
    }
    setLoading(false);
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Fertilizer Recommendation
      </Typography>
      <TextField
        label="Area Name"
        value={areaName}
        onChange={(e) => setAreaName(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Crop Type"
        value={cropType}
        onChange={(e) => setCropType(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Farm Size (acres)"
        value={farmSize}
        onChange={(e) => setFarmSize(e.target.value)}
        fullWidth
        margin="normal"
      />
      
      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : 'Get Recommendation'}
      </Button>
      {result && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">Recommendation Result:</Typography>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </Box>
      )}
    </Box>
  );
};

export default FertilizerRecommendation;