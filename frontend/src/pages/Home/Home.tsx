import React, { useEffect, useState, ChangeEvent } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Viagem {
  id: number;
  origem: string;
  destino: string;
  horario_partida: string;
  horario_chegada: string;
  dia_semana: number;
  valor: string;
  veiculo: number;
  motorista: number;
  is_pet_friendly: boolean;
  is_acessivel: boolean;
  is_ativo: boolean;
  veiculo_detalhes: {
    modelo: string;
    placa: string;
  };
  motorista_detalhes: {
    nome: string;
    telefone: string | null;
  };
}

interface Usuario {
  id: number;
  username: string;
  first_name: string;
  cidade: number;
  cidade_nome?: string;
  is_motorista: boolean;
}

interface Cidade {
  id: number;
  nome: string;
  estado: string;
}

interface FiltrosBusca {
  origem: string;
  destino: string;
  horario: string;
  preco: string;
}

const Home: React.FC = () => {
  const [viagens, setViagens] = useState<Viagem[]>([]);
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [cidades, setCidades] = useState<Cidade[]>([]);
  const [loading, setLoading] = useState(true);

  const [filtros, setFiltros] = useState<FiltrosBusca>({ origem: '', destino: '', horario: '', preco: '' });
  const [filtrosAtivos, setFiltrosAtivos] = useState(false);

  const fetchViagensPadrao = async (userLogado: Usuario) => {
    try {
      setLoading(true);
      const response = await api.get<Viagem[]>(`/viagens/?origem=${userLogado.cidade}`);
      const ordenadas = [...response.data].sort((a, b) => a.horario_partida.localeCompare(b.horario_partida));
      setViagens(ordenadas);
    } catch (error) {
      console.error("Erro ao buscar viagens padrão:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const carregarDadosIniciais = async () => {
      try {
        setLoading(true);
        const userResponse = await api.get<Usuario>('/me/');
        const userLogado = userResponse.data;
        setUsuario(userLogado);

        const cidadesResponse = await api.get<Cidade[]>('/cidades/');
        setCidades(cidadesResponse.data);

        await fetchViagensPadrao(userLogado);
      } catch (error) {
        console.error("Erro ao carregar dados do usuário:", error);
        setLoading(false);
      }
    };

    carregarDadosIniciais();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const handleFiltroChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFiltros((prev) => ({ ...prev, [name]: value }));
  };

  const aplicarFiltros = async () => {
    try {
      setLoading(true);
      
      const params: any = {};
      
      if (filtros.origem) params.origem = filtros.origem; 
      else if (usuario) params.origem = usuario.cidade; 
      
      if (filtros.destino) params.destino = filtros.destino; 
      if (filtros.horario) params.horario_partida = filtros.horario;
      if (filtros.preco) params.valor__lte = filtros.preco;

      const response = await api.get<Viagem[]>('/viagens/', { params });
      const ordenadas = [...response.data].sort((a, b) => a.horario_partida.localeCompare(b.horario_partida));
      
      setViagens(ordenadas);
      setFiltrosAtivos(true);
    } catch (error) {
      console.error("Erro ao aplicar filtros:", error);
    } finally {
      setLoading(false);
    }
  };

  const limparFiltros = () => {
    setFiltros({ origem: '', destino: '', horario: '', preco: '' });
    setFiltrosAtivos(false);
    if (usuario) fetchViagensPadrao(usuario);
  };

  const obterNomeCidade = (id: string | number) => {
    if (!id) return '';
    const cidade = cidades.find(c => c.id.toString() === id.toString());
    return cidade ? `${cidade.nome} - ${cidade.estado}` : id.toString();
  };

  const subtituloOrigem = filtrosAtivos && filtros.origem 
    ? `Saindo de: ${obterNomeCidade(filtros.origem)}` 
    : `Saindo de: ${usuario ? obterNomeCidade(usuario.cidade) : '...'}`;

  return (
    <div className="bg-light min-vh-100 pb-5">
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4">
        <div className="container">
          <span className="navbar-brand fw-bold">ROTA EXPRESSA</span>
          <div className="navbar-nav ms-auto align-items-center">
            {usuario?.is_motorista && (
              <Link to="/criar-viagem" className="btn btn-warning btn-sm me-3 fw-bold shadow-sm">
                ➕ NOVA VIAGEM
              </Link>
            )}
            <span className="nav-link active me-3">
              Olá, {usuario?.first_name || usuario?.username || 'Usuário'}
            </span>
            <button onClick={handleLogout} className="btn btn-outline-light btn-sm">
              Sair
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        
        <div className="card shadow-sm border-0 rounded-4 mb-4">
          <div className="card-body p-4">
            <h6 className="fw-bold text-primary mb-3 text-uppercase" style={{ fontSize: '0.85rem' }}>Filtros de Busca</h6>
            <div className="row g-3">
              <div className="col-md-3">
                <label className="form-label text-muted small fw-bold mb-1">Origem</label>
                <select className="form-select rounded-3" name="origem" value={filtros.origem} onChange={handleFiltroChange}>
                  <option value="">Qualquer origem</option>
                  {cidades.map(c => (
                    <option key={c.id} value={c.id}>{c.nome} - {c.estado}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-3">
                <label className="form-label text-muted small fw-bold mb-1">Destino</label>
                <select className="form-select rounded-3" name="destino" value={filtros.destino} onChange={handleFiltroChange}>
                  <option value="">Qualquer destino</option>
                  {cidades.map(c => (
                    <option key={c.id} value={c.id}>{c.nome} - {c.estado}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-3">
                <label className="form-label text-muted small fw-bold mb-1">A partir das:</label>
                <input type="time" className="form-control rounded-3" name="horario" value={filtros.horario} onChange={handleFiltroChange} />
              </div>
              <div className="col-md-3">
                <label className="form-label text-muted small fw-bold mb-1">Preço Máximo (R$)</label>
                <input type="number" step="0.01" min="0" className="form-control rounded-3" name="preco" placeholder="Ex: 50.00" value={filtros.preco} onChange={handleFiltroChange} />
              </div>
            </div>
            <div className="d-flex justify-content-end mt-3">
              {filtrosAtivos && (
                <button onClick={limparFiltros} className="btn btn-outline-secondary rounded-3 me-2 px-4">Limpar</button>
              )}
              <button onClick={aplicarFiltros} className="btn btn-primary rounded-3 px-4 fw-bold">BUSCAR</button>
            </div>
          </div>
        </div>

        <div className="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h2 className="h4 mb-0 fw-bold">Viagens Disponíveis</h2>
            <p className="text-muted small mb-0">{subtituloOrigem}</p>
          </div>
          <span className="badge bg-primary px-3 py-2 rounded-pill">
            {viagens.length} {viagens.length === 1 ? 'viagem encontrada' : 'viagens encontradas'}
          </span>
        </div>

        {loading ? (
          <div className="text-center mt-5">
            <div className="spinner-border text-primary" role="status"></div>
            <p className="mt-2 text-muted fw-bold">Buscando as melhores rotas...</p>
          </div>
        ) : (
          <div className="row">
            {viagens.map((viagem) => (
              <div key={viagem.id} className="col-12 mb-3">
                <div className="card shadow-sm border-0 border-start border-primary border-4 rounded-4 transition-hover">
                  <div className="card-body p-4">
                    <div className="row align-items-center">
                      
                      <div className="col-md-3 mb-3 mb-md-0">
                        <div className="d-flex justify-content-around align-items-center">
                          <div className="text-center">
                            <h4 className="mb-0 fw-bold">{viagem.horario_partida.substring(0, 5)}</h4>
                            <small className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.7rem' }}>Partida</small>
                          </div>
                          <div className="text-muted mx-2 fs-5">➔</div>
                          <div className="text-center">
                            <h4 className="mb-0 fw-bold">{viagem.horario_chegada.substring(0, 5)}</h4>
                            <small className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.7rem' }}>Chegada</small>
                          </div>
                        </div>
                      </div>

                      <div className="col-md-3 border-start mb-3 mb-md-0">
                        <p className="mb-0 text-muted small fw-bold text-uppercase" style={{ fontSize: '0.75rem' }}>Destino</p>
                        <h5 className="mb-0 fw-bold text-dark">{viagem.destino}</h5>
                      </div>

                      <div className="col-md-2 text-center mb-3 mb-md-0">
                        <div className="d-flex flex-column gap-2 align-items-center">
                          {viagem.is_pet_friendly && <span className="badge bg-info-subtle text-info border border-info-subtle w-100">🐾 Pet Friendly</span>}
                          {viagem.is_acessivel && <span className="badge bg-warning-subtle text-dark border border-warning-subtle w-100">♿ Acessível</span>}
                        </div>
                      </div>

                      <div className="col-md-2 text-center mb-3 mb-md-0">
                        <h3 className="text-success mb-0 fw-bold">R$ {viagem.valor}</h3>
                        <div className="small mt-1 fw-semibold">
                          {viagem.is_ativo ? (
                            <span className="text-primary">● Disponível</span>
                          ) : (
                            <span className="text-danger">● Indisponível</span>
                          )}
                        </div>
                      </div>

                      <div className="col-md-2 text-md-end text-center mt-3 mt-md-0">
                        <Link to={`/viagem/${viagem.id}`} className="btn btn-primary w-100 py-2 fw-bold rounded-3">
                          DETALHES
                        </Link>
                      </div>
                      
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && viagens.length === 0 && (
          <div className="card p-5 text-center shadow-sm border-0 rounded-4 mt-2">
            <div className="mb-3" style={{ fontSize: '3rem' }}>📍</div>
            <h5 className="fw-bold">Nenhuma viagem encontrada</h5>
            <p className="text-muted mb-0">Tente ajustar os filtros ou buscar por outras rotas e horários.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
