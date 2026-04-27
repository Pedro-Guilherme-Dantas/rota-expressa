import React, { useState, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../../../services/api';
import { AxiosError } from 'axios';
import '../Login/style.css'; 

interface Cidade {
  id: number;
  nome: string;
  estado: string;
}

export default function Registro() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    cidade: '',
    password: '',
    confirmPassword: '',
    is_motorista: false
  });

  const [cidades, setCidades] = useState<Cidade[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [showSuccessCard, setShowSuccessCard] = useState(false);

  useEffect(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    const fetchCidades = async () => {
      try {
        const response = await api.get<Cidade[]>('/cidades/');
        setCidades(response.data);
      } catch (err) {
        console.error("Erro ao carregar cidades:", err);
      }
    };
    fetchCidades();
  }, []);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'radio') {
      setFormData(prev => ({ ...prev, [name]: value === 'true' }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    if (formData.password !== formData.confirmPassword) {
      setError("As senhas não coincidem.");
      return;
    }

    if (formData.password.length < 8) {
      setError("A senha deve ter no mínimo 8 caracteres.");
      return;
    }

    if (!formData.cidade) {
      setError("Por favor, selecione sua cidade base.");
      return;
    }

    setLoading(true);

    const payload = {
      username: formData.username,
      first_name: formData.first_name,
      last_name: formData.last_name,
      email: formData.email,
      cidade: parseInt(formData.cidade, 10),
      password: formData.password,
      is_motorista: formData.is_motorista
    };

    try {
      await api.post('/usuarios/', payload);
      
      if (formData.is_motorista) {
        setShowSuccessCard(true);
      } else {
        navigate('/', { state: { message: 'Conta criada com sucesso! Faça login.' } });
      }
    } catch (err) {
      const axiosError = err as AxiosError<any>;
      const errorMessage = axiosError.response?.data?.detail 
        || JSON.stringify(axiosError.response?.data) 
        || "Erro ao criar conta. Verifique os dados.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (showSuccessCard) {
    return (
      <div className="bg-light min-vh-100 d-flex align-items-center justify-content-center p-3">
        <div className="card shadow-lg border-0 rounded-4 text-center p-5" style={{ maxWidth: '500px' }}>
          <div className="bg-success bg-opacity-10 text-success rounded-circle d-flex align-items-center justify-content-center mx-auto mb-4" style={{ width: '80px', height: '80px' }}>
            <span className="fs-1">✓</span>
          </div>
          <h3 className="fw-bold text-dark mb-3">Cadastro Concluído!</h3>
          <p className="text-muted mb-4" style={{ lineHeight: '1.6' }}>
            Sua solicitação de registro foi enviada para a staff, que analisará em até 24 horas. Entraremos em contato caso sejam necessárias informações adicionais.
          </p>
          <button 
            onClick={() => navigate('/')} 
            className="btn btn-primary w-100 py-3 fw-bold rounded-3 shadow-sm"
          >
            OK, ENTENDI
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-light min-vh-100 d-flex align-items-center justify-content-center py-5 px-3">
      <div className="card shadow-lg border-0 rounded-4 w-100" style={{ maxWidth: '600px' }}>
        <div className="card-body p-4 p-md-5">
          
          <div className="text-center mb-4">
            <div className="bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style={{ width: '60px', height: '60px' }}>
              <span className="fs-2">📝</span>
            </div>
            <h2 className="fw-bold text-dark mb-1">Crie sua Conta</h2>
            <p className="text-muted">Preencha seus dados para acessar a Rota Expressa</p>
          </div>

          {error && (
            <div className="alert alert-danger py-2 rounded-3 small text-center mb-4" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            
            <div className="mb-4">
              <label className="form-label text-muted small fw-bold mb-2">Qual será o seu perfil?</label>
              <div className="d-flex gap-3">
                <div className="form-check flex-fill bg-white border rounded-3 p-3 text-center shadow-sm position-relative" style={{ cursor: 'pointer' }}>
                  <input className="form-check-input float-none mx-auto d-block mb-2" type="radio" name="is_motorista" id="radioPassageiro" value="false" checked={!formData.is_motorista} onChange={handleChange} />
                  <label className="form-check-label fw-bold w-100 stretched-link" htmlFor="radioPassageiro" style={{ cursor: 'pointer' }}>
                    Quero apenas viajar
                  </label>
                </div>
                <div className="form-check flex-fill bg-white border rounded-3 p-3 text-center shadow-sm position-relative" style={{ cursor: 'pointer' }}>
                  <input className="form-check-input float-none mx-auto d-block mb-2" type="radio" name="is_motorista" id="radioMotorista" value="true" checked={formData.is_motorista} onChange={handleChange} />
                  <label className="form-check-label fw-bold w-100 stretched-link" htmlFor="radioMotorista" style={{ cursor: 'pointer' }}>
                    Quero ser Motorista
                  </label>
                </div>
              </div>
            </div>

            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <div className="form-floating">
                  <input type="text" className="form-control rounded-3" id="first_name" name="first_name" placeholder="Nome" value={formData.first_name} onChange={handleChange} required minLength={2} />
                  <label htmlFor="first_name" className="text-muted">Nome</label>
                </div>
              </div>
              <div className="col-md-6">
                <div className="form-floating">
                  <input type="text" className="form-control rounded-3" id="last_name" name="last_name" placeholder="Sobrenome" value={formData.last_name} onChange={handleChange} required minLength={2} />
                  <label htmlFor="last_name" className="text-muted">Sobrenome</label>
                </div>
              </div>
            </div>

            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <div className="form-floating">
                  <input type="text" className="form-control rounded-3" id="username" name="username" placeholder="Usuário" value={formData.username} onChange={handleChange} required minLength={3} />
                  <label htmlFor="username" className="text-muted">Nome de Usuário</label>
                </div>
              </div>
              <div className="col-md-6">
                <div className="form-floating">
                  <input type="email" className="form-control rounded-3" id="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                  <label htmlFor="email" className="text-muted">E-mail</label>
                </div>
              </div>
            </div>

            <div className="form-floating mb-3">
              <select className="form-select rounded-3" id="cidade" name="cidade" value={formData.cidade} onChange={handleChange} required>
                <option value="">Selecione sua cidade base...</option>
                {cidades.map(c => (
                  <option key={c.id} value={c.id}>{c.nome} - {c.estado}</option>
                ))}
              </select>
              <label htmlFor="cidade" className="text-muted">Cidade</label>
            </div>

            <div className="row g-3 mb-4">
              <div className="col-md-6">
                <div className="form-floating">
                  <input type="password" className="form-control rounded-3" id="password" name="password" placeholder="Senha" value={formData.password} onChange={handleChange} required minLength={8} />
                  <label htmlFor="password" className="text-muted">Senha (min. 8 chars)</label>
                </div>
              </div>
              <div className="col-md-6">
                <div className="form-floating">
                  <input type="password" className="form-control rounded-3" id="confirmPassword" name="confirmPassword" placeholder="Confirme a Senha" value={formData.confirmPassword} onChange={handleChange} required minLength={8} />
                  <label htmlFor="confirmPassword" className="text-muted">Confirmar Senha</label>
                </div>
              </div>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary w-100 py-3 fw-bold rounded-3 shadow-sm d-flex justify-content-center align-items-center"
              disabled={loading}
            >
              {loading ? (
                <div className="spinner-border spinner-border-sm text-white" role="status"></div>
              ) : (
                'FINALIZAR CADASTRO'
              )}
            </button>

          </form>

          <div className="text-center mt-4">
            <p className="text-muted mb-0 small">
              Já possui uma conta?{' '}
              <Link to="/" className="text-primary text-decoration-none fw-bold">
                Faça Login
              </Link>
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}
