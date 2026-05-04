# Rota Expressa - Plataforma Web para Otimização da Mobilidade Intermunicipal 🚗🛣️

<p align="center">
  <img src="https://img.shields.io/badge/Projeto-TCC-blue" alt="Projeto TCC">
  <img src="https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB" alt="Frontend React">
  <img src="https://img.shields.io/badge/Backend-Django%20REST-092E20" alt="Backend Django">
</p>

## 📌 Sobre o Projeto

O **Rota Expressa** é uma aplicação web de transporte intermunicipal desenvolvida para conectar passageiros a motoristas de forma simples, confiável e prática. Funcionando como um mural dinâmico de viagens agendadas, a plataforma facilita o encontro de pessoas com o mesmo destino.

> **Nota:** Este projeto foi desenvolvido como **Trabalho de Conclusão de Curso (TCC)** e seu objetivo principal é demonstrar uma solução viável para a otimização da mobilidade intermunicipal.

## 🎥 Demonstração

Confira o projeto em funcionamento através do vídeo de demonstração:

[![Demonstração do Projeto](https://img.youtube.com/vi/cD4GCEYEvEw/0.jpg)](https://youtu.be/cD4GCEYEvEw)


*(Clique na imagem acima para assistir ao vídeo no YouTube)*

## ✨ Principais Funcionalidades

- **Mural de Viagens:** Visualização dinâmica de viagens agendadas partindo da cidade de origem do usuário.
- **Conexão Direta:** Contato facilitado via WhatsApp diretamente com o motorista para confirmações e combinados.
- **Sem Intermediação Financeira:** O pagamento da viagem é acordado e realizado diretamente entre passageiro e motorista no momento do embarque.
- **Perfis Detalhados:** Avaliações de motoristas e informações sobre os veículos, incluindo regras como *Pet Friendly* e Acessibilidade (PCD).

## 🛠️ Tecnologias Utilizadas

O sistema foi dividido em duas partes principais, seguindo o modelo de separação de responsabilidades:

- **Frontend:** Desenvolvido com React, TypeScript, Vite e Bootstrap 5, oferecendo uma experiência fluida com visualização mobile-first.
- **Backend:** Desenvolvido em Python utilizando Django e Django Rest Framework (DRF) para criação de uma API REST robusta, JWT para autenticação, postgresql como banco de dados e Redis como servidor cache.

## 📂 Estrutura do Repositório

Como este repositório organiza tanto a interface quanto a API, o código está dividido em duas pastas principais. **Para detalhes técnicos, endpoints da API e instruções de instalação de cada ambiente, consulte os respectivos READMEs em cada pasta:**

- [`/frontend`](./frontend) - Contém todo o código da interface do usuário. Acesse o [README do Frontend](./frontend/README.md) para documentação técnica e passos de execução.
- [`/backend`](./backend) - Contém a API e a modelagem do banco de dados. Acesse o [README do Backend](./backend/README.md) para documentação e instruções de configuração da API.
- [`docker-compose.yml`](./docker-compose.yml) - Arquivo de orquestração caso deseje subir ambos os ambientes integrados via Docker.

