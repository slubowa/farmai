import React from 'react';
import { Box, Typography, Container } from '@mui/material';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Box component="footer" sx={{ bgcolor: 'background.paper', py: 3 }}>
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="left">
          © {currentYear} FarmAI
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
