import { Routes, Route } from 'react-router-dom';
import SideBar from '../components/sidebar.tsx';
import Models from '../pages/models';
import Model from '../pages/model';
import ModelVersion from '../pages/modelversion';
// import Account from '../pages/account';
// import Settings from '../pages/settings';
import { AppShell } from '@mantine/core';

function Home() {

    return (
        <AppShell
            padding="md"
            navbar={<SideBar />}
        >
            <Routes>
                <Route path="/" element={<Models/>} />
                <Route path="/model/:modelID" element={<Model/>} />
                <Route path="/model/:modelID/:modelVersion" element={<ModelVersion/>} />
                {/* <Route path="/account" element={<Account/>} />
                <Route path="/settings" element={<Settings/>} /> */}
            </Routes>
        </AppShell>
    )
}

export default Home;
