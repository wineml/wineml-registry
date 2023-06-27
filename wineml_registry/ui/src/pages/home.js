import { Routes, Route } from 'react-router-dom';
import Box from '@mui/material/Box';
import SideBar from '../components/sidebar.tsx';
import Models from '../pages/models';
import Model from '../pages/model';
import Account from '../pages/account';
import ModelVersion from '../pages/modelversion';
import Settings from '../pages/settings';

function Home() {

    return (
        <Box sx={{ display: 'flex' }}>
            <SideBar />
            <Box
                component="main"
                sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
            >
                <Routes>
                    <Route path="/" element={<Models/>} />
                    <Route path="/model/:modelID" element={<Model/>} />
                    <Route path="/model/:modelID/:modelVersion" element={<ModelVersion/>} />
                    <Route path="/account" element={<Account/>} />
                    <Route path="/settings" element={<Settings/>} />
                </Routes>
            </Box>
        </Box>
    )
}

export default Home;
