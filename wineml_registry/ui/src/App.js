import './App.css';
import AppRoutes from './routes';
import { AuthProvider } from './authContext';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { pink, red } from '@mui/material/colors';
import { alpha } from "@mui/material";


const theme = createTheme({
  palette: {
    primary: {
      main: pink[900],
      background: alpha(pink[900], 0.75),
    },
    secondary: {
      main: red[500],
    },
  },
});


function App() {

  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <AuthProvider>
          <main>
            <AppRoutes />
          </main>
        </AuthProvider>
      </div>
    </ThemeProvider>
  );
}

export default App;
