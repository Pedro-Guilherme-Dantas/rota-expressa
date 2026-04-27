import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import api from '../../services/api';

interface ViagemDetalhes {
  id: number;
  origem: string;
  destino: string;
  horario_partida: string;
  horario_chegada: string;
  valor: string;
  is_pet_friendly: boolean;
  is_acessivel: boolean;
  is_ativo: boolean;
  veiculo_detalhes: {
    modelo: string;
    placa: string;
  };
  motorista_detalhes: {
    nome: string;
    telefone: string;
  };
}

const ViagemDetalhes: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [viagem, setViagem] = useState<ViagemDetalhes | null>(null);
  const [loading, setLoading] = useState(true);
  const [mapaCarregado, setMapaCarregado] = useState(false);

  useEffect(() => {
    const fetchViagem = async () => {
      try {
        const response = await api.get<ViagemDetalhes>(`/viagens/${id}/`);
        setViagem(response.data);
      } catch (error) {
        console.error("Erro ao buscar detalhes da viagem:", error);
        navigate('/home'); 
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchViagem();
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
        <div className="spinner-border text-primary" role="status"></div>
      </div>
    );
  }

  if (!viagem) return null;

  const mensagemWhatsapp = encodeURIComponent(
    `Olá ${viagem.motorista_detalhes.nome}! Vi sua viagem de ${viagem.origem} para ${viagem.destino} no Rota Expressa e tenho interesse.`
  );

  return (
    <div className="bg-light min-vh-100 pb-5">
      <nav className="navbar navbar-dark bg-primary shadow-sm">
        <div className="container">
          <Link to="/home" className="btn btn-link text-white text-decoration-none p-0 d-flex align-items-center">
            <span className="fs-4 me-2">←</span> Voltar para viagens
          </Link>
        </div>
      </nav>

      <div className="w-100 bg-secondary position-relative d-flex justify-content-center align-items-center" style={{ height: '250px' }}>
        
        {!mapaCarregado && (
          <div className="position-absolute d-flex flex-column align-items-center text-white z-1">
            <div className="spinner-border mb-2" role="status" style={{ width: '2rem', height: '2rem' }}></div>
            <span className="fw-bold tracking-wide">Desenhando rota no mapa...</span>
          </div>
        )}

        <iframe
          title={`Rota de ${viagem.origem} para ${viagem.destino}`}
          width="100%"
          height="100%"
          style={{ 
            border: 0, 
            opacity: mapaCarregado ? 1 : 0, 
            transition: 'opacity 0.5s ease-in-out',
            zIndex: 2,
            position: 'relative'
          }}
          loading="lazy"
          allowFullScreen
          referrerPolicy="no-referrer-when-downgrade"
          onLoad={() => setMapaCarregado(true)}
          src={`https://www.google.com/maps/embed/v1/directions?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&origin=${encodeURIComponent(viagem.origem)}&destination=${encodeURIComponent(viagem.destino)}`}
        ></iframe>
      </div>

      <div className="container" style={{ marginTop: '-40px' }}>
        <div className="row">
          
          <div className="col-lg-8 mb-4">
            
            <div className="card shadow-sm border-0 mb-4 rounded-4">
              <div className="card-body p-4 p-md-5">
                <div className="d-flex justify-content-between align-items-center mb-4">
                  <h3 className="fw-bold mb-0">Detalhes do Trajeto</h3>
                  {viagem.is_ativo ? (
                    <span className="badge bg-success-subtle text-success border border-success px-3 py-2 fs-6">● Disponível</span>
                  ) : (
                    <span className="badge bg-danger-subtle text-danger border border-danger px-3 py-2 fs-6">● Lotado</span>
                  )}
                </div>

                <div className="position-relative ms-3 border-start border-3 border-primary py-2 ps-4">
                  {/* Origem */}
                  <div className="position-relative mb-4">
                    <div className="position-absolute bg-primary rounded-circle" style={{ width: '16px', height: '16px', left: '-33px', top: '4px' }}></div>
                    <h4 className="fw-bold mb-0">{viagem.horario_partida.substring(0, 5)}</h4>
                    <p className="text-muted fs-5 mb-0">{viagem.origem}</p>
                    <small className="text-primary fw-semibold">Local de Embarque</small>
                  </div>

                  {/* Destino */}
                  <div className="position-relative">
                    <div className="position-absolute bg-white border border-3 border-primary rounded-circle" style={{ width: '16px', height: '16px', left: '-33px', top: '4px' }}></div>
                    <h4 className="fw-bold mb-0">{viagem.horario_chegada.substring(0, 5)}</h4>
                    <p className="text-muted fs-5 mb-0">{viagem.destino}</p>
                    <small className="text-secondary fw-semibold">Local de Desembarque</small>
                  </div>
                </div>
              </div>
            </div>

            <div className="card shadow-sm border-0 rounded-4">
              <div className="card-body p-4">
                <h4 className="fw-bold mb-4">Informações do Veículo</h4>
                <div className="d-flex align-items-center">
                  <div className="bg-light rounded p-4 text-center me-4">
                    <div style={{ fontSize: '2.5rem' }}>🚐</div>
                  </div>
                  <div>
                    <h5 className="fw-bold mb-1">{viagem.veiculo_detalhes.modelo}</h5>
                    <p className="text-muted mb-2">Placa: <span className="text-uppercase bg-light border px-2 py-1 rounded">{viagem.veiculo_detalhes.placa}</span></p>
                    <div className="d-flex gap-2 mt-3">
                      {viagem.is_pet_friendly && <span className="badge bg-info text-dark">🐾 Aceita Pets</span>}
                      {viagem.is_acessivel && <span className="badge bg-warning text-dark">♿ Acessibilidade</span>}
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <div className="col-lg-4">
            
            <div className="card shadow-sm border-0 rounded-4 mb-4 text-center">
              <div className="card-body p-4">
                <Link 
                  to={`/motorista/${viagem.motorista}`} 
                  className="text-decoration-none shadow-hover"
                >
                  <div className="bg-secondary rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center text-white fw-bold fs-2" style={{ width: '80px', height: '80px' }}>
                    {viagem.motorista_detalhes.nome.charAt(0)}
                  </div>
                  <h5 className="fw-bold mb-1">{viagem.motorista_detalhes.nome}</h5>
                </Link>
                <p className="text-muted small mb-4">Motorista Verificado</p>

                {viagem.motorista_detalhes.telefone ? (
                  <a 
                    href={`https://wa.me/${viagem.motorista_detalhes.telefone}?text=${mensagemWhatsapp}`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn btn-success w-100 py-2 fw-bold d-flex align-items-center justify-content-center"
                  >
                    <span className="me-2 fs-5">📱</span> Falar no WhatsApp
                  </a>
                ) : (
                  <button className="btn btn-secondary w-100 py-2 fw-bold d-flex align-items-center justify-content-center" disabled>
                    <span className="me-2 fs-5">📱</span> Telefone indisponível
                  </button>
                )}
                <small className="text-muted mt-3 d-block">
                  A reserva de lugares é combinada diretamente com o motorista.
                </small>
              </div>
            </div>

            <div className="card shadow-sm border-0 rounded-4 border-top border-primary border-4">
              <div className="card-body p-4 text-center">
                <h6 className="text-muted text-uppercase fw-bold mb-3">Valor por Pessoa</h6>
                <h2 className="text-primary fw-bold display-5 mb-4">R$ {viagem.valor}</h2>
                
                <hr className="text-muted" />
                
                <div className="text-start mt-3">
                  <p className="fw-bold mb-2">Pagamento direto ao motorista via:</p>
                  <div className="d-flex flex-wrap gap-2">
                    <span className="badge border border-secondary text-dark bg-white px-3 py-2">PIX</span>
                    <span className="badge border border-secondary text-dark bg-white px-3 py-2">Dinheiro</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default ViagemDetalhes;