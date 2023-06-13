import { useContext } from 'react';
import { AuthContext } from '../authContext';
import { useNavigate } from 'react-router-dom';

import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import PieChartIcon from '@mui/icons-material/PieChart';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';



function SideBar() {
    const navigate = useNavigate();
    const { logout } = useContext(AuthContext);


    function handleHome() {
        navigate('/');
    }

    function handleLogout() {
        logout();
        window.location.reload();
    }

    return (
        <Drawer
            PaperProps={{
                sx: {
                backgroundColor: "primary.background"
                }
            }}
            sx={{
            width: 240,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
                width: 240,
                boxSizing: 'border-box',
                },
            color: 'black',
            }}
            variant="permanent"
            anchor="left"
        >
            <Toolbar>
                <h2 style={{color: 'black', textAlign: 'center', cursor: 'pointer'}} onClick={handleHome}>WineML</h2>
            </Toolbar>
            <Divider />
            <List>
                <ListItem key="models" disablePadding>
                    <ListItemButton onClick={() => {navigate("/models")}}>
                        <ListItemIcon>
                            <PieChartIcon />
                        </ListItemIcon>
                        <ListItemText primary="Models" />
                    </ListItemButton>
                </ListItem>
            </List>
            <Divider />
            <List>
                <ListItem key="account" disablePadding>
                    <ListItemButton onClick={() => {navigate("/account")}}>
                        <ListItemIcon>
                            <PersonIcon />
                        </ListItemIcon>
                        <ListItemText primary="Account" />
                    </ListItemButton>
                </ListItem>
                <ListItem key="logout" disablePadding>
                    <ListItemButton onClick={handleLogout}>
                        <ListItemIcon>
                            <ExitToAppIcon />
                        </ListItemIcon>
                        <ListItemText primary="Logout" />
                    </ListItemButton>
                </ListItem>
            </List>
        </Drawer>
    );
}

export default SideBar;
