import './App.css';
import AppRoutes from './routes';
import { AuthProvider } from './authContext';


function App() {

  return (
    <div className="App">
      <AuthProvider>
        <main>
          <AppRoutes />
        </main>
      </AuthProvider>
    </div>
  );
}

export default App;
