import { Routes, Route } from 'react-router-dom';
import Box from '@mui/material/Box';
import SideBar from '../components/sidebar';
import Dashboard from '../pages/dashboard';
import Models from '../pages/models';
import Model from '../pages/model';
import Account from '../pages/account';

function Home() {

    return (
        <Box sx={{ display: 'flex' }}>
            <SideBar />
            <Box
                component="main"
                sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
            >
                <Routes>
                    <Route path="/" element={<Dashboard/>} />
                    <Route path="/account" element={<Account/>} />
                    <Route path="/models" element={<Models/>} />
                    <Route path="/model" element={<Model/>} />
                </Routes>
            </Box>
        </Box>
    )
}

export default Home;
