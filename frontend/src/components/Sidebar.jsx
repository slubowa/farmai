import React from 'react';
import { List, ListItemButton, ListItemText, ListItemIcon, Box } from '@mui/material';
import { Link } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ScoreIcon from '@mui/icons-material/Score';
import LocalFloristIcon from '@mui/icons-material/LocalFlorist';

const SideBar = ({ items }) => {
  return (
    <Box sx={{ width: 250, bgcolor: '#2E7D32', color: 'white', height: '100vh', p: 2, boxShadow: 3 }}>
      <List>
        {items.map((item, index) => (
          <ListItemButton key={index} component={Link} to={item.path} sx={{ mb: 1, borderRadius: '5%', '&:hover': { bgcolor: '#388E3C' } }}>
            <ListItemIcon sx={{ color: 'white' }}>
              {item.icon === 'Home' && <HomeIcon />}
              {item.icon === 'Score' && <ScoreIcon />}
              {item.icon === 'LocalFlorist' && <LocalFloristIcon />}
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );
};

export default SideBar;