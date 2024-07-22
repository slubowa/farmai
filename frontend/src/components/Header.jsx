import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';

function Header() {
  return (
    <AppBar position="fixed">
      <Toolbar>
        <Button color="inherit" component={Link} to="/" startIcon={<HomeIcon />}>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            FarmAI Platform
          </Typography>
        </Button>
        <Button color="inherit" component={Link} to="/creditScoring">
          Credit Scoring
        </Button>
        <Button color="inherit" component={Link} to="/fertilizerRecommendation">
          Fertilizer Recommendation
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default Header;