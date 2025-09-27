<h1 align="center">
  Rede Cegonha: API de Acompanhamento Pré-Natal
</h1>

<blockquote align="center">“Cuidar do início da vida é construir um futuro saudável e promissor.”</blockquote>
<br>

<p align="center">
  <a href="#-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;  
  <a href="#-instalação-e-execução">Instalação e Execução</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-api">API</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-desenvolvedores">Desenvolvedores</a>
</p>

---

## 💻 Projeto

O **Rede Cegonha** é um sistema web para o acompanhamento pré-natal de gestantes. O projeto consiste em uma API RESTful robusta (Backend) e uma interface de usuário moderna e reativa (Frontend).

**Funcionalidades:**

- Autenticação de usuário segura baseada em sessão.
- Cadastro completo e busca de gestantes por CPF.
- Um cronograma pré-natal interativo para gerenciar consultas e exames, com status editáveis e salvamento de alterações.
- Utilitários como cálculo de semanas de gestação e preenchimento de endereço via CEP.

---

## 🧪 Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias e ferramentas:

### Backend (API)

- **Linguagem:** Python 3
- **Framework:** Flask
- **Banco de Dados:** SQLAlchemy com SQLite
- **Autenticação:** Sessão (Cookies)
- **Comunicação:** Flask-CORS
- **Testes:** Pytest

### Frontend (Interface)

- **Framework:** React com TypeScript
- **Build Tool:** Vite
- **Estilização:** Tailwind CSS
- **Roteamento:** React Router DOM
- **Cliente HTTP:** Axios
- **Testes:** Vitest + React Testing Library

---

## ⚙️ Instalação e Execução

O projeto é dividido em dois repositórios. Para a aplicação completa funcionar, o backend e o frontend precisam estar rodando simultaneamente em terminais separados.

### 1. Backend (Este Repositório)

```bash
# Clone este repositório
git clone [COLE AQUI A URL DO SEU REPOSITÓRIO BACKEND]
cd nome-da-pasta-do-backend

# Crie e ative o ambiente virtual
python -m venv venv
# No Windows (Git Bash):
source venv/Scripts/activate
# No Mac/Linux:
# source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
flask run --debug
```

## 📡 API

Nossa API possui 7 endpoints que cobrem autenticação e o gerenciamento de dados das gestantes (operações de CRUD).

### Autenticação

- Endpoint: /api/login
- Método: POST
- Protegida: Não

Descrição: Autentica um usuário com username e password e cria uma sessão no servidor.

- Endpoint: /api/logout
- Método: POST
- Protegida: Sim

Descrição: Encerra a sessão do usuário atual.

- Endpoint: /api/status
- Método: GET
- Protegida: Sim
  Descrição: Verifica se o usuário atual tem uma sessão ativa.

### Gestantes (CRUD)

- Endpoint: /api/gestantes
- Método: POST
- Protegida: Sim

Descrição: Cria um novo cadastro de gestante, recebendo os dados no corpo da requisição.

- Endpoint: /api/gestantes
- Método: GET
- Protegida: Sim

Descrição: Lê (busca) a lista completa de todas as gestantes cadastradas.

- Endpoint: /api/gestantes/<cpf>
- Método: GET
- Protegida: Sim

Descrição: Lê (busca) os dados de uma gestante específica pelo CPF.

- Endpoint: /api/gestantes/<cpf>
- Método: PUT
- Protegida: Sim
  Descrição: Atualiza os dados de uma gestante existente (ex: o cronograma).

---

## 🧑‍💻 Desenvolvedores

| Aluno                            | RA       |
| -------------------------------- | -------- |
| Adriano Alves do Nascimento      | 2230506  |
| Camila Nazare Pereira Gonçalves  | 23208252 |
| Erlandson Silva do Nascimento    | 2204739  |
| Fernando Caires Borges Goncalves | 23203515 |
| Klayton Rodrigues de Souza       | 2204509  |
| Marcia Alves Rodrigues da Silva  | 2201297  |
| Vinicius Torres Novaes           | 2214439  |
| Willians Soares de Souza         | 2229831  |

---
