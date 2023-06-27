import { useContext } from 'react';
import { AuthContext } from '../authContext';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from '../pages/home';
import Login from '../pages/login';


function AppRoutes() {
  const { isLoggedIn } = useContext(AuthContext);


  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={isLoggedIn ? <Home /> : <Login />} />
        <Route path="/home/*" element={isLoggedIn ? <Home /> : <Navigate to='/'/>} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
