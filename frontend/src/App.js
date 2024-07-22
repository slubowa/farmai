import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Container from '@mui/material/Container';
import { Grid, Box } from '@mui/material';
import FertilizerRecommendation from './components/fertilizerRecommendation';
import MainPage from './pages/mainPage';
import Header from './components/Header';
import Footer from './components/Footer';
import CreditScoring from './components/creditScoring';
import Chat from './components/chat';

function App() {
  return (
    <Router>
    <Header />
      <Container>
        <Box sx={{ my: 4, mt:10 }}>
          <Routes>
            <Route path="/" element={<Box><MainPage /></Box>} />
            <Route path="/fertilizerRecommendation" element={<FertilizerRecommendation />} />
            <Route path="/creditScoring" element={<CreditScoring />} />
          </Routes>
          <Grid item xs={12} sx={{ mt: 4 }}>
            <Box sx={{ p: 2, bgcolor: '#D9D9D9', borderRadius: '5%', boxShadow: 3 }}>
              <Chat />
            </Box>
          </Grid>
        </Box>
      </Container>
      <Footer />
    </Router>
  );
}

export default App;