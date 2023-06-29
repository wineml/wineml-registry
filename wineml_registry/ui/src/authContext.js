// AuthContext.js
import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [isLoggedIn, setLoggedIn] = useState(true); //TO REMOVE WHEN AUTH IS DONE
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedAuthState = localStorage.getItem('authState');

    if (storedAuthState) {
      const { isLoggedIn: storedIsLoggedIn, user: storedUser } = JSON.parse(storedAuthState);
      setLoggedIn(storedIsLoggedIn);
      setUser(storedUser);
    }
  }, []);

  const login = (userData) => {
    // Perform login logic, e.g., making API calls
    // Update isLoggedIn and user state based on the result
    // ...

    // Save the updated authentication state to localStorage
    localStorage.setItem('authState', JSON.stringify({ isLoggedIn: true, user: userData }));
  };

  const logout = () => {
    // Perform logout logic, e.g., clearing tokens or resetting user data
    // Update isLoggedIn and user state
    // ...

    // Clear the authentication state from localStorage
    localStorage.removeItem('authState');
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
