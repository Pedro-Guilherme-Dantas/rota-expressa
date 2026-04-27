import React, { useState, useEffect, useCallback, type ChangeEvent, type FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import AsyncSelect from 'react-select/async';
import api from '../../services/api';
import { AxiosError } from 'axios';

interface CidadeIBGE {
  id: number;
  nome: string;
  microrregiao: {
    mesorregiao: {
      UF: {
        sigla: string;
      }
    }
  }
}

interface OptionType {
  value: string;
  label: string;
  nome: string;
  estado: string;
  searchLabel: string;
}

interface Veiculo {
  id: number;
  placa: string;
  modelo_nome?: string;
}

interface FormData {
  horario_partida: string;
  horario_chegada: string;
  dia_semana: string;
  valor: string;
  veiculo: string;
  is_pet_friendly: boolean;
  is_acessivel: boolean;
  is_ativo: boolean;
}

const DIAS_SEMANA = [
  { valor: 0, rotulo: 'Segunda-feira' },
  { valor: 1, rotulo: 'Terça-feira' },
  { valor: 2, rotulo: 'Quarta-feira' },
  { valor: 3, rotulo: 'Quinta-feira' },
  { valor: 4, rotulo: 'Sexta-feira' },
  { valor: 5, rotulo: 'Sábado' },
  { valor: 6, rotulo: 'Domingo' },
];

let cacheCidadesIBGE: OptionType[] | null = null;

const buscarCidadesIBGE = async (inputValue: string): Promise<OptionType[]> => {
  if (inputValue.length < 3) return [];
  
  if (!cacheCidadesIBGE) {
    try {
      const res = await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/municipios');
      const data: CidadeIBGE[] = await res.json();
      cacheCidadesIBGE = data
        .filter(c => c.microrregiao?.mesorregiao?.UF?.sigla)
        .map(c => {
          const siglaUF = c.microrregiao.mesorregiao.UF.sigla;
          const labelStr = `${c.nome} - ${siglaUF}`;
          return {
            value: `${c.nome}-${siglaUF}`,
            label: labelStr,
            nome: c.nome,
            estado: siglaUF,
            searchLabel: labelStr.normalize('NFD').replace(/[\u0300-\u036f]/g, "").toLowerCase(),
          };
        });
    } catch {
      return [];
    }
  }

  const searchInput = inputValue.normalize('NFD').replace(/[\u0300-\u036f]/g, "").toLowerCase();
  return cacheCidadesIBGE
    .filter(c => c.searchLabel.includes(searchInput))
    .slice(0, 20); 
};

export default function CriarViagem() {
  const navigate = useNavigate();

  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  
  const [cidadeOrigem, setCidadeOrigem] = useState<OptionType | null>(null);
  const [cidadeDestino, setCidadeDestino] = useState<OptionType | null>(null);

  const [loadingDados, setLoadingDados] = useState(true);
  const [loadingSubmit, setLoadingSubmit] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<FormData>({
    horario_partida: '',
    horario_chegada: '',
    dia_semana: '',
    valor: '',
    veiculo: '',
    is_pet_friendly: false,
    is_acessivel: false,
    is_ativo: true,
  });

  const loadCidadesOptions = useCallback(buscarCidadesIBGE, []);

  useEffect(() => {
    const fetchVeiculos = async () => {
      try {
        setLoadingDados(true);
        const veiculosRes = await api.get<Veiculo[]>('/veiculos/');
        setVeiculos(veiculosRes.data);
      } catch (err) {
        console.error("Erro ao carregar veículos:", err);
        setError("Erro ao carregar veículos.");
      } finally {
        setLoadingDados(false);
      }
    };
    fetchVeiculos();
  }, []);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setFormData((prev) => ({ ...prev, [name]: checked }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    if (!cidadeOrigem || !cidadeDestino) {
      setError("Por favor, selecione a cidade de origem e a cidade de destino.");
      return;
    }

    setLoadingSubmit(true);

    const payload = {
      ...formData,
      origem_nome: cidadeOrigem.nome,
      origem_estado: cidadeOrigem.estado,
      destino_nome: cidadeDestino.nome,
      destino_estado: cidadeDestino.estado,
    };

    try {
      await api.post('/viagens/', payload);
      navigate('/home'); 
    } catch (err) {
      const axiosError = err as AxiosError<any>;
      const errorMessage = axiosError.response?.data?.detail 
        || "Erro ao criar a viagem. Verifique os dados e tente novamente.";
      setError(JSON.stringify(axiosError.response?.data) || errorMessage);
    } finally {
      setLoadingSubmit(false);
    }
  };

  if (loadingDados) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
        <div className="spinner-border text-primary" role="status"></div>
      </div>
    );
  }

  return (
    <div className="bg-light min-vh-100 pb-5">
      <nav className="navbar navbar-dark bg-primary shadow-sm mb-4">
        <div className="container">
          <Link to="/home" className="btn btn-link text-white text-decoration-none p-0 d-flex align-items-center">
            <span className="fs-4 me-2">←</span> Voltar
          </Link>
          <span className="navbar-brand fw-bold mb-0">Nova Viagem</span>
        </div>
      </nav>

      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-8">
            <div className="card shadow-lg border-0 rounded-4">
              <div className="card-body p-4 p-md-5">
                
                <div className="text-center mb-4">
                  <h2 className="fw-bold text-dark mb-1">Agendar Nova Viagem</h2>
                  <p className="text-muted">Preencha os dados do trajeto e do veículo</p>
                </div>

                {error && (
                  <div className="alert alert-danger rounded-3 small mb-4" role="alert">
                    {error}
                  </div>
                )}

                <form onSubmit={handleSubmit}>
                  
                  <h6 className="fw-bold text-primary mb-3 text-uppercase" style={{ fontSize: '0.85rem' }}>Trajeto</h6>
                  <div className="row mb-4">
                    <div className="col-md-6 mb-3 mb-md-0">
                      <label className="form-label text-muted small fw-bold mb-1">Origem</label>
                      <AsyncSelect
                        loadOptions={loadCidadesOptions}
                        value={cidadeOrigem}
                        onChange={(option) => setCidadeOrigem(option as OptionType)}
                        placeholder="Digite o nome da cidade..."
                        isClearable
                        noOptionsMessage={({ inputValue }) =>
                          inputValue.length < 3 ? 'Digite pelo menos 3 letras' : 'Cidade não encontrada'
                        }
                        loadingMessage={() => 'Buscando cidades...'}
                      />
                    </div>
                    
                    <div className="col-md-6">
                      <label className="form-label text-muted small fw-bold mb-1">Destino</label>
                      <AsyncSelect
                        loadOptions={loadCidadesOptions}
                        value={cidadeDestino}
                        onChange={(option) => setCidadeDestino(option as OptionType)}
                        placeholder="Digite o nome da cidade..."
                        isClearable
                        noOptionsMessage={({ inputValue }) =>
                          inputValue.length < 3 ? 'Digite pelo menos 3 letras' : 'Cidade não encontrada'
                        }
                        loadingMessage={() => 'Buscando cidades...'}
                      />
                    </div>
                  </div>

                  <h6 className="fw-bold text-primary mb-3 text-uppercase" style={{ fontSize: '0.85rem' }}>Horários</h6>
                  <div className="row mb-4">
                    <div className="col-md-4 mb-3 mb-md-0">
                      <div className="form-floating">
                        <select className="form-select rounded-3" name="dia_semana" value={formData.dia_semana} onChange={handleChange} required>
                          <option value="">Dia da semana</option>
                          {DIAS_SEMANA.map((dia) => (
                            <option key={dia.valor} value={dia.valor}>{dia.rotulo}</option>
                          ))}
                        </select>
                        <label>Dia da Semana</label>
                      </div>
                    </div>
                    <div className="col-md-4 mb-3 mb-md-0">
                      <div className="form-floating">
                        <input type="time" className="form-control rounded-3" name="horario_partida" value={formData.horario_partida} onChange={handleChange} required />
                        <label>Horário de Partida</label>
                      </div>
                    </div>
                    <div className="col-md-4">
                      <div className="form-floating">
                        <input type="time" className="form-control rounded-3" name="horario_chegada" value={formData.horario_chegada} onChange={handleChange} required />
                        <label>Horário de Chegada</label>
                      </div>
                    </div>
                  </div>

                  <h6 className="fw-bold text-primary mb-3 text-uppercase" style={{ fontSize: '0.85rem' }}>Detalhes da Viagem</h6>
                  <div className="row mb-4">
                    <div className="col-md-6 mb-3 mb-md-0">
                      <div className="form-floating">
                        <input type="number" step="0.01" min="0" className="form-control rounded-3" name="valor" placeholder="Ex: 50.00" value={formData.valor} onChange={handleChange} required />
                        <label>Valor da Passagem (R$)</label>
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="form-floating">
                        <select className="form-select rounded-3" name="veiculo" value={formData.veiculo} onChange={handleChange} required>
                          <option value="">Selecione um veículo</option>
                          {veiculos.map((v) => (
                            <option key={v.id} value={v.id}>{v.modelo_nome || 'Veículo'} - {v.placa}</option>
                          ))}
                        </select>
                        <label>Veículo Utilizado</label>
                      </div>
                    </div>
                  </div>

                  <h6 className="fw-bold text-primary mb-3 text-uppercase" style={{ fontSize: '0.85rem' }}>Características</h6>
                  <div className="bg-light p-3 rounded-3 border mb-4">
                    <div className="form-check form-switch mb-2">
                      <input className="form-check-input" type="checkbox" role="switch" id="pet_friendly" name="is_pet_friendly" checked={formData.is_pet_friendly} onChange={handleCheckboxChange} />
                      <label className="form-check-label" htmlFor="pet_friendly">Aceita Pets (Pet Friendly)</label>
                    </div>
                    <div className="form-check form-switch mb-2">
                      <input className="form-check-input" type="checkbox" role="switch" id="acessivel" name="is_acessivel" checked={formData.is_acessivel} onChange={handleCheckboxChange} />
                      <label className="form-check-label" htmlFor="acessivel">Veículo Acessível (PCD)</label>
                    </div>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="ativo" name="is_ativo" checked={formData.is_ativo} onChange={handleCheckboxChange} />
                      <label className="form-check-label" htmlFor="ativo">Viagem Ativa (Aparecerá nas buscas)</label>
                    </div>
                  </div>

                  <button 
                    type="submit" 
                    className="btn btn-primary w-100 py-3 fw-bold rounded-3 shadow-sm d-flex justify-content-center align-items-center mt-2"
                    disabled={loadingSubmit}
                  >
                    {loadingSubmit ? (
                      <div className="spinner-border spinner-border-sm text-white" role="status"></div>
                    ) : (
                      'CRIAR VIAGEM'
                    )}
                  </button>

                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}