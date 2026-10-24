# 🛡️ Sentinel API

**API experimental de análise de riscos e monitoramento de eventos de segurança, desenvolvida com Python e JavaScript.**

A Sentinel API é um projeto de portfólio que demonstra como validar eventos, analisar indicadores de risco, aplicar políticas de segurança e registrar eventos para auditoria por meio de uma arquitetura dividida em quatro camadas.

O projeto utiliza Python, FastAPI, Pydantic e Node.js para demonstrar conceitos de desenvolvimento de APIs, validação de dados, análise de risco baseada em regras, comunicação entre serviços e registro estruturado de eventos.

> **Status:** protótipo funcional em ambiente local. Não é um produto de segurança financeira pronto para produção.

---

## 📌 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Objetivos](#-objetivos)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Execução](#-execução)
- [Documentação da API](#-documentação-da-api)
- [Endpoints](#-endpoints)
- [Exemplo de requisição](#-exemplo-de-requisição)
- [Análise de risco](#-análise-de-risco)
- [Segurança](#-segurança)
- [Testes](#-testes)
- [Limitações](#-limitações)
- [Melhorias futuras](#-melhorias-futuras)
- [Licença](#-licença)

---

## 🔎 Sobre o projeto

A Sentinel API foi criada para explorar uma arquitetura modular de análise de eventos de segurança.

A aplicação recebe informações sobre um evento, valida os dados recebidos, calcula uma pontuação de risco e aplica uma política que recomenda uma ação.

Os eventos podem representar situações como:

- Tentativas de login;
- Requisições HTTP;
- Operações de checkout;
- Acessos a dados.

A API não coleta automaticamente esses dados de bancos, sites ou sistemas de pagamento. As informações devem ser fornecidas por um sistema integrado.

## 🎯 Objetivos

- Desenvolver uma API REST com FastAPI;
- Validar dados usando Pydantic;
- Implementar regras de análise de risco em Python;
- Criar um motor de políticas em JavaScript;
- Registrar eventos para auditoria;
- Aplicar autenticação por chave de API;
- Demonstrar comunicação HTTP entre serviços;
- Organizar o código em módulos com responsabilidades distintas;
- Praticar testes automatizados e documentação técnica.

---

## ⚙️ Funcionalidades

### 1. Validação de dados

Verifica a estrutura dos eventos recebidos, os tipos de dados e os campos permitidos.

### 2. Análise de risco

Calcula uma pontuação com base em indicadores definidos no motor de regras.

### 3. Classificação de risco

Classifica os eventos em três níveis:

| Pontuação | Nível | Interpretação |
|---|---|---|
| 0–29 | Baixo | Poucos indicadores de risco foram acionados |
| 30–69 | Médio | Os indicadores justificam atenção |
| 70–100 | Alto | Os indicadores justificam revisão adicional |

Esses limites são regras demonstrativas e não constituem uma escala universal de risco.

### 4. Aplicação de políticas

O serviço JavaScript interpreta a avaliação e recomenda uma ação:

- `allow`: não recomendar ação adicional;
- `monitor`: recomendar monitoramento;
- `review`: recomendar revisão adicional.

As ações são recomendações da aplicação. Elas não bloqueiam automaticamente transações ou requisições em sistemas externos.

### 5. Registro de auditoria

Registra eventos processados em formato JSONL, permitindo análise posterior.

### 6. Autenticação

A API principal utiliza uma chave de API. A comunicação interna entre os serviços utiliza uma chave separada.

### 7. Documentação interativa

O FastAPI fornece uma interface para consultar e testar os endpoints.

---

## 🏗️ Arquitetura

O projeto é dividido em quatro camadas.

### Camada 1 — Validação Python

**Arquivo:** `app/python_layer_1/validation.py`

Responsável por validar os dados recebidos e garantir que os eventos respeitem o formato definido.

Tecnologia principal: Pydantic.

### Camada 2 — Motor de risco Python

**Arquivo:** `app/python_layer_2/risk_engine.py`

Analisa os indicadores, calcula a pontuação e determina a classificação de risco.

Tecnologia principal: Python.

### Camada 3 — Motor de políticas JavaScript

**Arquivo:** `javascript_layer_3/policy_engine.js`

Recebe a avaliação de risco, valida os dados recebidos pelo serviço interno, aplica a política de decisão e solicita o registro do evento.

Tecnologia principal: Node.js.

### Camada 4 — Auditoria JavaScript

**Arquivo:** `javascript_layer_4/audit_logger.js`

Registra os resultados em um arquivo JSONL.

Tecnologias principais: JavaScript e sistema de arquivos do Node.js.

### Fluxo de processamento

```text
Sistema integrado
       |
       v
API principal — FastAPI
       |
       v
Camada 1 — Validação Python
       |
       v
Camada 2 — Análise de risco Python
       |
       | Comunicação HTTP interna
       v
Camada 3 — Políticas JavaScript
       |
       v
Camada 4 — Auditoria JavaScript
       |
       v
Resposta JSON
```

---

## 🧰 Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python | API principal e análise de risco |
| FastAPI | Construção dos endpoints |
| Pydantic | Validação de dados |
| Uvicorn | Servidor da aplicação Python |
| HTTPX | Comunicação HTTP entre serviços |
| Node.js | Execução dos serviços JavaScript |
| JavaScript | Políticas e auditoria |
| dotenv | Leitura de variáveis de ambiente |
| Pytest | Testes automatizados |
| JSON | Formato de requisições e respostas |
| JSONL | Registro estruturado de eventos |
| Git | Controle de versão |

---

## 📁 Estrutura do projeto

```text
sentinel-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── python_layer_1/
│   │   ├── __init__.py
│   │   └── validation.py
│   └── python_layer_2/
│       ├── __init__.py
│       └── risk_engine.py
├── javascript_layer_3/
│   └── policy_engine.js
├── javascript_layer_4/
│   └── audit_logger.js
├── tests/
│   └── test_validation.py
├── .env.example
├── .gitignore
├── package.json
├── package-lock.json
├── requirements.txt
└── README.md
```

A pasta `logs/` é criada durante a execução, quando um evento é registrado.

Arquivos como `.env`, `.venv`, `node_modules` e logs locais devem permanecer fora do repositório público.

---

## 💻 Requisitos

Para executar o projeto, você precisará de:

- Python 3.11 ou superior;
- Node.js 20 ou superior;
- npm;
- Git.

Os comandos abaixo utilizam o PowerShell no Windows.

---

## 🚀 Instalação

### 1. Clone o repositório

Depois de publicar o projeto, utilize:

```bash
git clone https://github.com/SEU-USUARIO/sentinel-api.git
cd sentinel-api
```

Substitua `SEU-USUARIO` pelo seu usuário do GitHub.

### 2. Crie o ambiente virtual Python

```powershell
python -m venv .venv
```

Ative-o:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências Python

```powershell
python -m pip install -r requirements.txt
```

### 4. Instale as dependências JavaScript

Na raiz do projeto, execute:

```powershell
npm install
```

---

## 🔐 Configuração

Crie um arquivo `.env` na raiz do projeto.

Exemplo de configuração:

```dotenv
SENTINEL_API_KEY=SUBSTITUA_POR_UMA_CHAVE_SECRETA
SENTINEL_INTERNAL_KEY=SUBSTITUA_POR_OUTRA_CHAVE_SECRETA
POLICY_PORT=3001
POLICY_URL=http://127.0.0.1:3001/evaluate
```

Gere duas chaves aleatórias diferentes com Python:

```powershell
python -c "import secrets; print('API:', secrets.token_urlsafe(48)); print('INTERNAL:', secrets.token_urlsafe(48))"
```

Copie os valores gerados para as variáveis correspondentes no arquivo `.env`.

**Não publique o `.env` nem compartilhe suas chaves secretas.** O arquivo `.env.example` deve conter apenas valores fictícios.

---

## ▶️ Execução

A aplicação utiliza dois serviços que precisam estar ativos ao mesmo tempo.

### Terminal 1 — Serviço JavaScript

Na raiz do projeto:

```powershell
npm start
```

O serviço deverá apresentar uma mensagem semelhante a:

```text
Sentinel policy engine listening on 127.0.0.1:3001
```

Mantenha esse terminal aberto.

### Terminal 2 — API Python

Ative o ambiente virtual, se necessário:

```powershell
.\.venv\Scripts\Activate.ps1
```

Inicie a API:

```powershell
python -m uvicorn app.main:app --reload
```

A aplicação ficará disponível localmente em:

```text
http://127.0.0.1:8000
```

O parâmetro `--reload` é destinado ao desenvolvimento.

---

## 📚 Documentação da API

Com o serviço Python em execução, abra:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

A documentação permite consultar os endpoints e enviar requisições de teste.

Esses endereços são locais e não ficam disponíveis publicamente na internet.

---

## 🔌 Endpoints

### `GET /health`

Verifica se a API principal está respondendo.

Exemplo:

```powershell
curl.exe http://127.0.0.1:8000/health
```

### `POST /v1/analyze`

Recebe um evento, valida os dados, calcula o risco e solicita a aplicação da política JavaScript.

O endpoint exige o cabeçalho `X-API-Key`.

---

## 🧪 Exemplo de requisição

Endpoint:

```text
POST http://127.0.0.1:8000/v1/analyze
```

Cabeçalho:

```http
Content-Type: application/json
X-API-Key: SUA_CHAVE_DE_API
```

Corpo JSON:

```json
{
  "event_type": "login",
  "requests_last_minute": 150,
  "failed_attempts": 8,
  "unique_accounts": 12,
  "sensitive_data_exposed": false
}
```

### Descrição dos campos

| Campo | Tipo | Descrição |
|---|---|---|
| `event_type` | String | Tipo de evento observado |
| `requests_last_minute` | Inteiro | Número de requisições observadas no último minuto |
| `failed_attempts` | Inteiro | Número de tentativas malsucedidas |
| `unique_accounts` | Inteiro | Quantidade de contas distintas observadas |
| `sensitive_data_exposed` | Booleano | Indica se foi reportada exposição de dados sensíveis |

Os tipos de evento aceitos são `login`, `checkout`, `data_access` e `api_request`.

Os dados devem ser fornecidos pelo sistema integrado. A Sentinel não coleta essas informações automaticamente.

---

## 📤 Exemplo de resposta

Para o exemplo acima, a resposta esperada é semelhante a:

```json
{
  "score": 70,
  "level": "high",
  "reasons": [
    "High request volume",
    "Multiple failed attempts",
    "Multiple accounts observed"
  ],
  "action": "review",
  "message": "High risk: additional security review recommended."
}
```

Esse resultado é ilustrativo. A resposta exata depende das regras implementadas no código.

---

## 🧮 Análise de risco

O motor de risco utiliza regras explícitas para atribuir pontos.

| Indicador | Condição demonstrativa | Pontos |
|---|---|---:|
| Volume elevado | 100 ou mais requisições por minuto | +25 |
| Tentativas malsucedidas | 5 ou mais | +25 |
| Contas distintas | 10 ou mais | +20 |
| Exposição de dados | Valor verdadeiro | +50 |

A pontuação final é limitada a 100.

### Exemplo de cálculo

```text
Volume elevado:       +25
Tentativas falhas:    +25
Contas distintas:     +20
Exposição de dados:    +0
--------------------------
Pontuação final:       70
Classificação:        HIGH
```

As regras são simples e foram definidas para fins educacionais. Em ambientes reais, é necessário avaliar contexto, qualidade dos dados, falsos positivos e impacto das decisões.

---

## 🔒 Segurança

O projeto demonstra mecanismos básicos de proteção:

- Autenticação da API por chave;
- Chave separada para comunicação interna;
- Validação dos dados de entrada;
- Limite para o tamanho do corpo HTTP no serviço JavaScript;
- Registro estruturado de eventos.

### Considerações para produção

Antes de utilizar uma solução desse tipo para proteger sistemas reais, seria necessário implementar e testar mecanismos adicionais, como:

- HTTPS e configuração segura de rede;
- Limitação de requisições;
- Rotação e gestão de segredos;
- Autorização efetiva das operações protegidas;
- Armazenamento de auditoria protegido contra alterações;
- Monitoramento, alertas e recuperação de falhas;
- Testes de integração, carga e segurança;
- Políticas de privacidade e retenção de dados;
- Revisão independente do código.

A Sentinel não substitui um firewall, WAF, sistema de detecção de intrusão ou os controles de segurança de uma instituição financeira.

---

## 🧪 Testes

O projeto inclui testes automatizados com Pytest.

Execute:

```powershell
python -m pytest -v
```

Os testes existentes verificam aspectos da validação de dados.

A cobertura completa de todas as camadas e de todos os cenários de segurança ainda precisa ser avaliada.

---

## ⚠️ Limitações

A versão atual é um protótipo educacional e de portfólio.

Entre as limitações:

- A análise utiliza regras fixas;
- Os eventos são fornecidos por um sistema integrado;
- Não há coleta automática de telemetria;
- A auditoria utiliza arquivo local;
- As ações são recomendações, não bloqueios efetivos;
- Não há integração pronta com bancos, checkouts ou gateways de pagamento;
- Não existe garantia de detecção de todos os ataques;
- A implantação em produção exige controles adicionais.

---

## 🛣️ Melhorias futuras

Possíveis evoluções incluem:

- Ampliar os testes de integração;
- Adicionar limitação de requisições;
- Implementar métricas e alertas;
- Melhorar o tratamento de falhas entre serviços;
- Criar políticas configuráveis;
- Implementar testes de carga;
- Adicionar armazenamento centralizado de auditoria;
- Criar uma integração demonstrativa com uma aplicação;
- Automatizar testes com integração contínua;
- Documentar uma implantação segura.

---

## 🤝 Contribuição

Contribuições são bem-vindas.

1. Faça um fork do repositório.
2. Crie uma branch para sua alteração.
3. Implemente a melhoria.
4. Execute os testes.
5. Abra um pull request explicando as mudanças.

---

## 📄 Licença

Nenhuma licença foi definida nesta versão.

Antes de permitir formalmente a reutilização e distribuição do projeto por terceiros, escolha uma licença e adicione um arquivo `LICENSE` ao repositório.

---

## 👨‍💻 Sobre

**Sentinel API** é um projeto de portfólio voltado ao estudo de desenvolvimento de APIs, validação de dados, análise de risco e arquitetura modular com Python e JavaScript.

**Tecnologias principais:** Python · FastAPI · Pydantic · Node.js · JavaScript · HTTP · Pytest
