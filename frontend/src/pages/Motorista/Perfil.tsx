import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface UsuarioInfo {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  cidade: number;
  date_joined: string;
}

interface MotoristaPerfil {
  id: number;
  usuario: UsuarioInfo;
  nota_media: number;
  resumo: string;
}

interface Avaliacao {
  id: number;
  usuario: number;
  motorista: number;
  nota: number;
  comentario: string;
}

const PerfilMotorista: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [motorista, setMotorista] = useState<MotoristaPerfil | null>(null);
  const [loading, setLoading] = useState(true);

  const [avaliacaoId, setAvaliacaoId] = useState<number | null>(null);
  const [nota, setNota] = useState<number>(0);
  const [hoverNota, setHoverNota] = useState<number>(0);
  const [comentario, setComentario] = useState<string>('');
  const [enviandoAvaliacao, setEnviandoAvaliacao] = useState(false);
  const [feedback, setFeedback] = useState<{ tipo: 'sucesso' | 'erro'; mensagem: string } | null>(null);

  useEffect(() => {
    const fetchDados = async () => {
      try {
        setLoading(true);
        
        const [resMotorista, resMe] = await Promise.all([
          api.get<MotoristaPerfil>(`/motoristas/${id}/`),
          api.get('/me/')
        ]);
        setMotorista(resMotorista.data);
        const userLogadoId = resMe.data.id;

        const resAvaliacao = await api.get<Avaliacao[]>(`/avaliacoes/?motorista=${id}`);
        
        if (resAvaliacao.data && resAvaliacao.data.length > 0) {
          const minhaAvaliacao = resAvaliacao.data.find(aval => aval.usuario === userLogadoId);
          if (minhaAvaliacao) {
            setAvaliacaoId(minhaAvaliacao.id);
            setNota(minhaAvaliacao.nota);
            setComentario(minhaAvaliacao.comentario || '');
          }
        }
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
        if (!motorista) navigate('/home'); 
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchDados();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, navigate]);

  const renderizarEstrelas = (nota: number) => {
    const estrelas = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= Math.round(nota)) {
        estrelas.push(<span key={i} className="text-warning fs-4">★</span>);
      } else {
        estrelas.push(<span key={i} className="text-muted opacity-25 fs-4">★</span>);
      }
    }
    return estrelas;
  };

  const handleAvaliar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (nota === 0) {
      setFeedback({ tipo: 'erro', mensagem: 'Por favor, selecione uma nota de 1 a 5 estrelas.' });
      return;
    }

    setEnviandoAvaliacao(true);
    setFeedback(null);

    const payload = {
      motorista: parseInt(id as string, 10),
      nota: nota,
      comentario: comentario
    };

    try {
      if (avaliacaoId) {
        await api.patch(`/avaliacoes/${avaliacaoId}/`, payload);
        setFeedback({ tipo: 'sucesso', mensagem: 'Sua avaliação foi atualizada com sucesso!' });
      } else {
        const res = await api.post('/avaliacoes/', payload);
        setAvaliacaoId(res.data.id); 
        setFeedback({ tipo: 'sucesso', mensagem: 'Avaliação enviada com sucesso! Obrigado pelo feedback.' });
      }
      
      const resMotorista = await api.get<MotoristaPerfil>(`/motoristas/${id}/`);
      setMotorista(resMotorista.data);
      
    } catch (error: any) {
      console.error("Erro detalhado:", error.response?.data);
      setFeedback({ tipo: 'erro', mensagem: 'Ocorreu um erro ao processar sua avaliação. Tente novamente.' });
    } finally {
      setEnviandoAvaliacao(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
        <div className="spinner-border text-primary" role="status"></div>
      </div>
    );
  }

  if (!motorista) return null;

  const dataEntrada = new Date(motorista.usuario.date_joined).toLocaleDateString('pt-BR', {
    month: 'long',
    year: 'numeric'
  });

  return (
    <div className="bg-light min-vh-100 pb-5">
      <nav className="navbar navbar-dark bg-primary shadow-sm">
        <div className="container">
          <button onClick={() => navigate(-1)} className="btn btn-link text-white text-decoration-none p-0 d-flex align-items-center">
            <span className="fs-4 me-2">←</span> Voltar
          </button>
        </div>
      </nav>

      <div className="w-100 bg-primary bg-opacity-75" style={{ height: '150px' }}></div>

      <div className="container" style={{ marginTop: '-75px' }}>
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            
            <div className="card shadow-lg border-0 rounded-4 mb-4 text-center position-relative">
              <div className="card-body p-4 p-md-5">
                
                <div 
                  className="bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center mx-auto shadow fw-bold border border-4 border-white"
                  style={{ width: '120px', height: '120px', fontSize: '3rem', marginTop: '-80px', backgroundColor: '#6c757d' }}
                >
                  {motorista.usuario.first_name.charAt(0).toUpperCase()}
                </div>

                <h2 className="fw-bold mt-3 mb-1">
                  {motorista.usuario.first_name} {motorista.usuario.last_name}
                </h2>
                <p className="text-muted small mb-3">
                  Parceiro(a) desde {dataEntrada}
                </p>

                <div className="bg-light rounded-4 p-3 d-inline-block mb-4 shadow-sm border">
                  <div className="d-flex align-items-center justify-content-center gap-2">
                    <h3 className="fw-bold text-dark mb-0">{motorista.nota_media.toFixed(1)}</h3>
                    <div className="d-flex align-items-center mt-1">
                      {renderizarEstrelas(motorista.nota_media)}
                    </div>
                  </div>
                  <small className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.7rem' }}>
                    Nota Média Geral
                  </small>
                </div>

                <div className="text-start bg-white border rounded-4 p-4 shadow-sm">
                  <h6 className="fw-bold text-primary mb-3 text-uppercase" style={{ fontSize: '0.85rem', letterSpacing: '1px' }}>
                    Sobre o Motorista
                  </h6>
                  <p className="text-dark mb-0" style={{ lineHeight: '1.6' }}>
                    {motorista.resumo ? (
                      motorista.resumo
                    ) : (
                      <span className="text-muted fst-italic">Este motorista ainda não adicionou um resumo ao perfil.</span>
                    )}
                  </p>
                </div>

              </div>
            </div>

            <div className="card shadow-sm border-0 rounded-4 mb-4">
              <div className="card-body p-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h6 className="fw-bold text-primary mb-0 text-uppercase" style={{ fontSize: '0.85rem', letterSpacing: '1px' }}>
                    {avaliacaoId ? 'Sua Avaliação' : 'Avaliar Motorista'}
                  </h6>
                  {avaliacaoId && (
                    <span className="badge bg-info-subtle text-info border border-info-subtle rounded-pill px-3 py-2">
                      Já avaliado
                    </span>
                  )}
                </div>
                
                {feedback && (
                  <div className={`alert alert-${feedback.tipo === 'sucesso' ? 'success' : 'danger'} rounded-3 small mb-4`} role="alert">
                    {feedback.mensagem}
                  </div>
                )}

                <form onSubmit={handleAvaliar}>
                  <div className="mb-3 text-center">
                    <label className="form-label text-muted small fw-bold mb-2">Selecione uma nota</label>
                    <div className="d-flex justify-content-center gap-2">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <span
                          key={star}
                          className={`fs-1 ${star <= (hoverNota || nota) ? 'text-warning' : 'text-muted opacity-25'}`}
                          style={{ cursor: 'pointer', transition: 'color 0.2s' }}
                          onClick={() => setNota(star)}
                          onMouseEnter={() => setHoverNota(star)}
                          onMouseLeave={() => setHoverNota(0)}
                        >
                          ★
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mb-3">
                    <div className="form-floating">
                      <textarea 
                        className="form-control rounded-3" 
                        placeholder="Deixe um comentário (opcional)" 
                        id="comentario" 
                        style={{ height: '100px' }}
                        value={comentario}
                        onChange={(e) => setComentario(e.target.value)}
                      ></textarea>
                      <label htmlFor="comentario">Comentário (Opcional)</label>
                    </div>
                  </div>

                  <button 
                    type="submit" 
                    className={`btn ${avaliacaoId ? 'btn-outline-primary' : 'btn-primary'} w-100 py-3 fw-bold rounded-3 shadow-sm d-flex justify-content-center align-items-center transition-all`}
                    disabled={enviandoAvaliacao}
                  >
                    {enviandoAvaliacao ? (
                      <div className="spinner-border spinner-border-sm" role="status"></div>
                    ) : (
                      avaliacaoId ? 'ATUALIZAR AVALIAÇÃO' : 'ENVIAR AVALIAÇÃO'
                    )}
                  </button>
                </form>
              </div>
            </div>

            <div className="text-center text-muted small px-4">
              <p>🛡️ Os motoristas da <strong>Rota Expressa</strong> são avaliados continuamente pela comunidade para garantir viagens seguras e confortáveis.</p>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default PerfilMotorista;