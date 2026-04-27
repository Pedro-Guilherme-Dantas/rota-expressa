import './style.css'; 
import { useState, type ChangeEvent, type FormEvent } from 'react';
import api from '../../../services/api';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { AxiosError } from 'axios';

interface LoginResponse {
  access: string;
  refresh: string;
}

interface ApiErrorData {
  detail?: string;
}

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const successMessage = location.state?.message;
  const sessionExpiredMessage = searchParams.get('sessao_expirada')
    ? (searchParams.get('msg') || 'Sua sessão expirou. Por favor, faça login novamente.')
    : null;

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post<LoginResponse>('/token/', {
        username,
        password,
      });

      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      
      navigate('/home');
    } catch (err) {
      const axiosError = err as AxiosError<ApiErrorData>;
      const errorMessage = axiosError.response?.data?.detail || 'Credenciais inválidas. Tente novamente.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-light min-vh-100 d-flex align-items-center justify-content-center p-3">
      <div className="card shadow-lg border-0 rounded-4 w-100" style={{ maxWidth: '450px' }}>
        <div className="card-body p-5">
          
          <div className="text-center mb-5">
            <div className="bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style={{ width: '60px', height: '60px' }}>
              <span className="fs-2">🚌</span>
            </div>
            <h2 className="fw-bold text-dark mb-1">Login</h2>
            <p className="text-muted">Acesse sua conta para continuar</p>
          </div>

          <form onSubmit={handleSubmit}>
            
            <div className="form-floating mb-3">
              <input
                type="text"
                className="form-control rounded-3"
                id="username"
                placeholder="nome@exemplo.com"
                value={username}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
                required
              />
              <label htmlFor="username" className="text-muted">Email ou Usuário</label>
            </div>

            <div className="form-floating mb-4">
              <input
                type="password"
                className="form-control rounded-3"
                id="password"
                placeholder="Senha"
                value={password}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                required
              />
              <label htmlFor="password" className="text-muted">Senha</label>
            </div>

            {sessionExpiredMessage && (
              <div className="alert alert-warning py-2 rounded-3 small text-center" role="alert">
                🔒 {sessionExpiredMessage}
              </div>
            )}

            {successMessage && !error && (
              <div className="alert alert-success py-2 rounded-3 small text-center" role="alert">
                {successMessage}
              </div>
            )}
            
            {error && (
              <div className="alert alert-danger py-2 rounded-3 small text-center" role="alert">
                {error}
              </div>
            )}

            <button 
              type="submit" 
              className="btn btn-primary w-100 py-3 fw-bold rounded-3 shadow-sm d-flex justify-content-center align-items-center"
              disabled={loading}
            >
              {loading ? (
                <div className="spinner-border spinner-border-sm text-white" role="status"></div>
              ) : (
                'ENTRAR'
              )}
            </button>

          </form>

          <div className="text-center mt-4">
            <p className="text-muted mb-0 small">
              Ainda não tem uma conta?{' '}
              <Link to="/registro" className="text-primary text-decoration-none fw-bold">
                Registre-se aqui
              </Link>
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}