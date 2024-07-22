import { Grid, Box, Toolbar, Typography, Link } from '@mui/material';
import SideBar from '../components/Sidebar';
import React from 'react';

const MainPage = () => {
  const drawerItems = [
    { label: 'Home', path: '/', icon: 'Home' },
    { label: 'Credit Scoring', path: '/creditScoring', icon: 'Score' },
    { label: 'Fertilizer Recommendation', path: '/fertilizerRecommendation', icon: 'LocalFlorist' },
  ];

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f4f4f9' }}>
      <SideBar items={drawerItems} />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom>
              This platform helps farmers with credit scoring and fertilizer recommendations.
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Box sx={{ textAlign: 'center' }}>
              <img
                src="/farm.jpg"
                alt="Farmer in the field"
                style={{ width: '100%', height: '400px', borderRadius: '5%', boxShadow: '3' }}
              />
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Link href="/fertilizerRecommendation" underline="none">
              <Box sx={{ bgcolor: '#D9EAD3', p: 2, borderRadius: '5%', textAlign: 'center', boxShadow: 3 }}>
                <Typography variant="h6">Fertilizer Recommendation</Typography>
              </Box>
            </Link>
          </Grid>
          <Grid item xs={12} md={6}>
            <Link href="/creditScoring" underline="none">
              <Box sx={{ bgcolor: '#FFE599', p: 2, borderRadius: '5%', textAlign: 'center', boxShadow: 3 }}>
                <Typography variant="h6">Credit Scoring</Typography>
              </Box>
            </Link>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default MainPage;