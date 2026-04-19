# Rota Expressa - Backend


## 🚀 Tecnologias e Arquitetura

Tecnologias principais:
- **Linguagem / Framework**: Python 3, Django, Django Rest Framework (DRF)
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis (via backend nativo do Django)
- **Autenticação**: JSON Web Tokens (JWT) com `rest_framework_simplejwt`
- **Orquestração**: Docker e Docker Compose

### Padrões de Projeto (Design Patterns)
1. **Camada de Serviço (Service Layer)**: As regras de negócio pesadas e o acesso direto ao ORM (banco de dados) não ficam nas Views. As Views atuam apenas como Controladores HTTP. Todo o processamento é delegado aos arquivos na pasta `rota-expressa/services/`.
2. **Serializadores Duplos**: Utilizamos um padrão com dois serializers para cada entidade. Um `Serializer` padrão para escrita (recebendo apenas IDs de relações) e um `ResponseSerializer` para leitura (retornando objetos aninhados e formatados para economizar requisições do front-end).
3. **N+1 Queries Mitigado**: As buscas no banco utilizam `select_related` nos services para evitar chamadas excessivas ao banco em endpoints de listagem.

---

## 🛠️ Como Executar

O projeto já está configurado para rodar isoladamente através de containers.

1. Na raiz do projeto (onde está o `docker-compose.yml`), execute:
   ```bash
   docker compose up -d db redis web
   ```
2. O servidor rodará na porta `8000`. 
3. Você pode acessar a documentação interativa do Swagger gerada pelo `drf-spectacular` em: `http://localhost:8000/api/docs/swagger/`.

---

## 🔗 Endpoints da API

URL base: `/api/`

### 🔐 Autenticação
- `POST /api/token/`: Gera um par de tokens JWT (access_token, refresh_token).
- `POST /api/token/refresh/`: Renova um access token expirado.

### 🧑‍💻 Usuários e Perfis
- `GET/POST /api/usuarios/`: Cadastro e listagem de passageiros.
- `GET /api/me/`: Endpoint customizado que retorna todas as informações do usuário atual baseado no token JWT enviado (incluindo ID da cidade para filtro de viagens).
- `GET/POST /api/motoristas/`: Listagem e criação de perfis de motorista (extensão do usuário).

### 🚗 Transporte
- `GET/POST /api/veiculos/`: Gerenciamento da frota. O usuário (motorista logado) é injetado automaticamente na criação.
- `GET/POST /api/modelos/`: Tipos de veículos disponíveis.
- `GET/POST /api/viagens/`: O mural de viagens (coração do sistema).
  - **Filtros suportados**: `?origem=X`, `?destino=Y`, `?horario_partida=Z`, `?valor__lte=W`.
  - O motorista é injetado dinamicamente durante o `POST` baseado no token do usuário.

### 🗺️ Localidades
- `GET/POST /api/cidades/`: Cadastro e listagem de cidades suportadas. Rotas GET cacheadas por 24h.

### ⭐ Qualidade
- `GET/POST /api/avaliacoes/`: Avaliações dadas por passageiros aos motoristas.
- `GET/POST /api/telefones/`: Gerenciamento de contato direto para a desintermediação via WhatsApp.
