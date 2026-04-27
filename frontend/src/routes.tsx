import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Auth/Login/Login';
import Registro from './pages/Auth/Registro/Registro';
import Home from './pages/Home/Home';
import Viagem from './pages/Viagem/Viagem';
import CriarViagem from './pages/Viagem/CriarViagem';
import PerfilMotorista from './pages/Motorista/Perfil';
import PrivateRoute from './components/PrivateRoute';

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/registro" element={<Registro />} />

        <Route path="/home" element={<PrivateRoute><Home /></PrivateRoute>} />
        <Route path="/viagem/:id" element={<PrivateRoute><Viagem /></PrivateRoute>} />
        <Route path="/motorista/:id" element={<PrivateRoute><PerfilMotorista /></PrivateRoute>} />
        <Route path="/criar-viagem" element={<PrivateRoute><CriarViagem /></PrivateRoute>} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;