# importa-pdf

API REST para importar arquivos PDF de uma pasta. Esta API encontra um arquivo PDF em uma pasta configurada, retorna o arquivo via HTTP e o apaga após o envio.

## Funcionalidades

- ✅ Verifica se existe um arquivo PDF em uma pasta
- ✅ Retorna o primeiro PDF encontrado via HTTP
- ✅ Apaga o arquivo PDF após o envio
- ✅ Integração fácil com Bubble e outras plataformas

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/cassioxrocha/importa-pdf.git
cd importa-pdf
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. (Opcional) Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

## Configuração

Você pode configurar a API através de variáveis de ambiente:

- `PDF_FOLDER_PATH`: Caminho da pasta onde os PDFs serão procurados (padrão: `./pdfs`)
- `API_PORT`: Porta onde a API será executada (padrão: `8000`)
- `API_HOST`: Host da API (padrão: `0.0.0.0`)

## Uso

### Iniciar a API

```bash
python main.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em `http://localhost:8000`

### Endpoints

#### `GET /get-pdf`
**Endpoint principal:** Retorna o primeiro PDF encontrado na pasta e o apaga.

**Resposta de sucesso (200):**
- Retorna o arquivo PDF com headers apropriados
- O arquivo é apagado da pasta após o envio

**Resposta de erro (404):**
```json
{
  "detail": "Nenhum arquivo PDF encontrado na pasta"
}
```

**Exemplo de uso com cURL:**
```bash
curl -O http://localhost:8000/get-pdf
```

**Exemplo de uso com Bubble:**
Configure uma API call no Bubble:
- URL: `http://seu-servidor:8000/get-pdf`
- Method: GET
- Use as file type: PDF

#### `GET /check-pdf`
Verifica se existe um PDF na pasta **sem apagá-lo**. Útil para testes.

**Resposta de sucesso:**
```json
{
  "found": true,
  "filename": "documento.pdf",
  "size_bytes": 102400,
  "path": "/caminho/completo/documento.pdf"
}
```

**Resposta quando não há PDF:**
```json
{
  "found": false,
  "message": "Nenhum arquivo PDF encontrado na pasta"
}
```

#### `GET /health`
Health check da API.

**Resposta:**
```json
{
  "status": "healthy"
}
```

#### `GET /`
Informações básicas da API.

## Estrutura do Projeto

```
importa-pdf/
├── main.py              # Aplicação FastAPI principal
├── requirements.txt     # Dependências Python
├── .env.example        # Exemplo de configuração
├── .gitignore          # Arquivos ignorados pelo Git
├── README.md           # Documentação
└── pdfs/               # Pasta padrão para PDFs (criada automaticamente)
```

## Desenvolvimento

### Adicionar PDFs de teste

Crie a pasta `pdfs` e adicione arquivos PDF para testar:
```bash
mkdir -p pdfs
# Adicione seus PDFs de teste na pasta pdfs/
```

### Testes manuais

1. Adicione um PDF na pasta `pdfs/`
2. Verifique se existe PDF:
```bash
curl http://localhost:8000/check-pdf
```

3. Baixe e apague o PDF:
```bash
curl -O http://localhost:8000/get-pdf
```

4. Verifique novamente (deve retornar "not found"):
```bash
curl http://localhost:8000/check-pdf
```

## Deployment

### Opção 1: Docker Compose (Recomendado)

1. Construa e execute o container:
```bash
docker-compose up -d
```

2. A API estará disponível em `http://localhost:8000`

3. Os PDFs devem ser colocados na pasta `./pdfs` (mapeada para o container)

4. Para parar:
```bash
docker-compose down
```

### Opção 2: Docker Manual

1. Construa a imagem:
```bash
docker build -t importa-pdf .
```

2. Execute o container:
```bash
docker run -d -p 8000:8000 -v $(pwd)/pdfs:/app/pdfs importa-pdf
```

### Opção 3: Servidor Linux (Systemd)

1. Instale as dependências:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Crie um arquivo de serviço systemd em `/etc/systemd/system/importa-pdf.service`:
```ini
[Unit]
Description=PDF Import API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/importa-pdf
Environment="PATH=/opt/importa-pdf/venv/bin"
ExecStart=/opt/importa-pdf/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Inicie o serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl enable importa-pdf
sudo systemctl start importa-pdf
```

### Considerações de Produção

- ✅ Configure volumes persistentes para a pasta de PDFs
- ✅ Use variáveis de ambiente para configuração
- ⚠️ Considere adicionar autenticação/autorização se necessário
- ⚠️ Configure CORS se a API for chamada de um navegador
- ⚠️ Coloque atrás de um proxy reverso (nginx/traefik) com HTTPS
- ⚠️ Configure logs estruturados para monitoramento
- ⚠️ Implemente rate limiting para prevenir abuso

## Licença

MIT License
