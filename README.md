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

### Docker (Exemplo)

Crie um `Dockerfile` para deployment:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
RUN mkdir -p pdfs
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Considerações de Produção

- Configure volumes persistentes para a pasta de PDFs
- Use variáveis de ambiente para configuração
- Considere adicionar autenticação/autorização se necessário
- Configure CORS se a API for chamada de um navegador
- Implemente logs estruturados para monitoramento

## Licença

MIT License
