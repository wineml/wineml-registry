import { AuthContext } from '../authContext';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from '@mantine/form';
import {
  TextInput,
  PasswordInput,
  Paper,
  Title,
  Container,
  Button,
} from '@mantine/core';


function Login() {
    const navigate = useNavigate();
    const { login } = useContext(AuthContext);
    const form = useForm({
      initialValues: { email: '', password: '' },
      validate: {
        email: (val) => (/^\S+@\S+$/.test(val) ? null : 'Invalid email'),
        password: (val) => (val.length <= 6 ? 'Password should include at least 6 characters' : null),
      },
    });

    function handleLogin(values) {
      let email = values.email;
      let password = values.password;
      login({ email, password })
      navigate('/home');
    }

    return (
    <Container size={420} my="50%">
      <form onSubmit={(values) => handleLogin(values)}>
        <Paper shadow="xl" p={30} mt={30} radius="md">
          <Title
            align="center"
            sx={(theme) => ({ fontFamily: `Greycliff CF, ${theme.fontFamily}`, fontWeight: 600 })}
          >
            WineML
          </Title>
          <TextInput
            label="Email"
            required
            {...form.getInputProps('email')}
          />
          <PasswordInput
            label="Password"
            required
            {...form.getInputProps('password')}
            mt="md"
          />
          <Button fullWidth type="submit" mt="xl">Sign in</Button>
        </Paper>
      </form>
    </Container>
    )
}

export default Login;
