# IARA API Chatbot

Desenvolvimento da **API de Chatbot do projeto IARA**, responsável por realizar o **atendimento automatizado aos usuários** do aplicativo móvel, fornecendo respostas a perguntas frequentes e suporte interativo por meio de **inteligência artificial**.

A API utiliza o modelo **Gemini (Google Generative AI)** para processar mensagens e gerar respostas dinâmicas, integrando-se aos demais módulos do ecossistema **IARA**.

---

## 📚 Sumário

* [💡 Sobre o Projeto](#-sobre-o-projeto)
* [⚙️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
* [🧩 Como Executar](#-como-executar)
* [🧰 Endpoints / Exemplos de Uso](#-endpoints--exemplos-de-uso)
* [👩‍💻 Autor](#-autor)

---

## 💡 Sobre o Projeto

O **IARA Chatbot API** é uma aplicação desenvolvida em **Python (FastAPI)** com o objetivo de oferecer **atendimento automatizado** dentro do aplicativo **IARA Mobile**.

Esta API é responsável por:

* Processar mensagens de usuários e gerar respostas inteligentes via **Gemini API**.
* Autenticar usuários e gerenciar **tokens JWT**.
* Armazenar e recuperar **sessões de conversas**.
* Fazer upload e gerenciamento de **embeddings** (para compreensão semântica).
* Servir como interface entre o **usuário final** e o **módulo de IA** do sistema IARA.

---

## ⚙️ Tecnologias Utilizadas

| Categoria                         | Tecnologias                                                                   |
| --------------------------------- | ----------------------------------------------------------------------------- |
| **Linguagem**                     | Python 3.10+                                                                  |
| **Framework**                     | FastAPI                                                                       |
| **Servidor**                      | Uvicorn                                                                       |
| **IA**                            | Google Gemini API                                                             |
| **Autenticação**                  | JWT (JSON Web Token)                                                          |
| **Gerenciamento de Dependências** | pip / venv                                                                    |
| **Bibliotecas Principais**        | `fastapi`, `uvicorn`, `python-dotenv`, `requests`, `pandas`, `numpy`, `PyJWT` |

---

## 🧩 Como Executar

### 🐳 Usando Docker

```bash
# Cria a imagem
docker build -t iara-api-chatbot .

# Executa o container
docker run -p 8000:8000 iara-api-chatbot
```

---

### 🧱 Executando Localmente

```bash
# Clone o repositório
git clone https://github.com/IARA-TECH/iara-api-chatbot.git

# Acesse o diretório
cd iara-api-chatbot

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie o arquivo .env com as variáveis necessárias
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Execute o servidor
uvicorn app.main:app --reload
```

> ⚠️ **Importante:**
> Antes de iniciar a aplicação, configure corretamente a variável `GEMINI_API_KEY`.
> O servidor ficará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 🧰 Endpoints / Exemplos de Uso

### 🔹 Principais Endpoints

|  Método   | Endpoint            | Descrição                                               |
| :-------: | :-----------------: | :-----------------------------------------------------: |
|  `POST`   | `/auth/login`       | Realiza login e gera token JWT                          |
|  `POST`   | `/auth/verify`      | Valida token de autenticação                            |
|  `POST`   | `/chat`             | Envia mensagem do usuário e retorna resposta do chatbot |
|  `POST`   | `/embedding/upload` | Faz upload de arquivos de embeddings                    |
|  `GET`    | `/session/all`      | Lista todas as sessões de conversas                     |
|  `DELETE` | `/session/{id}`     | Exclui uma sessão específica                            |
|  `GET`    | `/docs`             | Acessa a documentação interativa (Swagger UI)           |

---

### 💬 Exemplo de Requisição

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
        "message": "Olá, preciso de ajuda com meu exame periódico"
      }'
```

**Resposta:**

```json
{
  "response": "Olá! Posso te ajudar com informações sobre seus exames periódicos. Qual dúvida você tem?"
}
```

---

## 👩‍💻 Autor

**IARA Tech**

Projeto interdisciplinar desenvolvido por alunos do **Instituto J&F**, como parte do ecossistema de soluções **IARA**, voltado à **automação de processos e atendimento inteligente**.

📍 São Paulo, Brasil
📧 [iaratech.oficial@gmail.com](mailto:iaratech.oficial@gmail.com)
🌐 GitHub: [https://github.com/IARA-TECH](https://github.com/IARA-TECH)

---
