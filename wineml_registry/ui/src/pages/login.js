import { AuthContext } from '../authContext';
import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';



function Login() {
    const navigate = useNavigate();
    const { login } = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    function handleLogin() {
        login({ email, password })
        navigate('/home');
    }

    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        height="100vh"
        position="relative"
        bgcolor="primary.background"
      >
        <Box
          width={300}
          p={8}
          border="1px solid #ccc"
          boxShadow={10}
          bgcolor="white"
          sx={{
            pt: 4,
            pb: 6,
          }}
        >
          <Typography variant="h6" align="center" mb={2}>
            WineML
          </Typography>
          <form onSubmit={handleLogin}>
            <Box mb={2}>
              <TextField
                fullWidth
                label="Email"
                variant="outlined"
                onChange={(e) => setEmail(e.target.value)}
              />
            </Box>
            <Box mb={2}>
              <TextField
                fullWidth
                label="Password"
                variant="outlined"
                type="password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </Box>
            <Button
              variant="contained"
              color="primary"
              type="submit"
              sx={{ width: '30%', alignSelf: 'flex-start' }}
            >
              Submit
            </Button>
          </form>
        </Box>
      </Box>
    )
}

export default Login;
