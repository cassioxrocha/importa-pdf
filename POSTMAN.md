# 📮 Testando no Postman

## 🚀 Como testar a API no Postman

### 1. **Inicie a API primeiro:**
```bash
python api.py
```

### 2. **Endpoints para testar:**

#### ✅ **Verificar Status**
- **Método:** `GET`
- **URL:** `http://localhost:5000/status`
- **Descrição:** Mostra arquivos na pasta e status do monitoramento

#### ✅ **Processar Arquivo**
- **Método:** `GET` 
- **URL:** `http://localhost:5000/process`
- **Descrição:** Move primeiro arquivo da pasta input para output e retorna em **base64**

#### 🔔 **Ver Notificações**
- **Método:** `GET`
- **URL:** `http://localhost:5000/notifications`
- **Descrição:** Lista todas as notificações de PDFs detectados

#### 🔔 **Última Notificação**
- **Método:** `GET`
- **URL:** `http://localhost:5000/notifications/latest`
- **Descrição:** Retorna apenas a última notificação (ideal para polling)

#### 🧹 **Limpar Notificações**
- **Método:** `POST`
- **URL:** `http://localhost:5000/notifications/clear`
- **Descrição:** Remove todas as notificações

#### 👀 **Controle do Monitor**
- **Método:** `POST`
- **URL:** `http://localhost:5000/monitor/start`
- **Descrição:** Inicia o monitoramento da pasta

- **Método:** `POST`
- **URL:** `http://localhost:5000/monitor/stop`
- **Descrição:** Para o monitoramento da pasta

#### 🔗 **Configurar Webhook**
- **Método:** `POST`
- **URL:** `http://localhost:5000/webhook/configure`
- **Body (JSON):**
```json
{
  "webhook_url": "https://seu-app.bubbleapps.io/api/1.1/wf/pdf-detected",
  "active": true
}
```
- **Descrição:** Configura webhook para notificar Bubble automaticamente

#### 🔗 **Status do Webhook**
- **Método:** `GET`
- **URL:** `http://localhost:5000/webhook/status`
- **Descrição:** Verifica se webhook está configurado

#### 🔗 **Testar Webhook**
- **Método:** `POST`
- **URL:** `http://localhost:5000/webhook/test`
- **Descrição:** Envia notificação de teste para o webhook

#### 📄 **Processar Arquivo Específico**
- **Método:** `GET`
- **URL:** `http://localhost:5000/process/nome-do-arquivo.pdf`
- **Descrição:** Processa arquivo específico por nome

### 3. **Fluxo de teste com monitoramento:**

1. **Inicie a API** - O monitoramento já começa automaticamente
2. **Teste /status** - Verifique que `monitoring_active: true`
3. **Coloque um PDF** na pasta `input/` 
4. **Teste /notifications/latest** - Veja a notificação do PDF detectado
5. **Teste /process** - Processe o arquivo e receba em base64
6. **Teste /notifications** - Veja histórico completo

### 🔄 **Como funciona o monitoramento:**

- ✅ **Automático:** Inicia junto com a API
- ✅ **Tempo real:** Detecta PDFs instantaneamente 
- ✅ **Notificações:** Armazena alertas com timestamp
- ✅ **Webhook:** Notifica Bubble automaticamente (recomendado)
- ✅ **Polling:** Use `/notifications/latest` para verificar novos PDFs

### 🎯 **Fluxo com Webhook (Recomendado para Bubble):**

1. **Configure webhook:** `POST /webhook/configure`
2. **Coloque PDF** na pasta `input/`
3. **API detecta** e envia webhook automaticamente para Bubble
4. **Bubble recebe** dados instantaneamente
5. **Bubble chama** `/process/nome-arquivo.pdf` para obter base64

### 4. **Responses esperados:**

**GET /status** (com arquivo na pasta):
```json
{
  "status": "ok",
  "files_in_input": 1,
  "file_names": ["exemplo.pdf"],
  "monitoring_active": true
}
```

**GET /notifications/latest** (quando PDF é detectado):
```json
{
  "status": "new_notification",
  "notification": {
    "timestamp": "2025-10-17T09:30:15.123456",
    "event": "pdf_added",
    "filename": "documento.pdf",
    "path": "input/documento.pdf",
    "message": "📄 Novo PDF detectado: documento.pdf"
  }
}
```

**GET /notifications** (histórico):
```json
{
  "status": "ok",
  "total_notifications": 3,
  "notifications": [...]
}
```

**GET /status** (sem arquivos):
```json
{
  "status": "ok", 
  "files_in_input": 0,
  "file_names": []
}
```

**GET /process** (com arquivo):
```json
{
  "status": "success",
  "filename": "exemplo.pdf",
  "file_size": 524,
  "file_base64": "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMi...",
  "moved_to": "output/exemplo.pdf"
}
```
- Retorna arquivo em **base64** (compatível com Bubble)
- Move arquivo de `input/` para `output/`

**GET /process** (sem arquivo):
```json
{
  "status": "no_files",
  "message": "Nenhum arquivo encontrado na pasta input"
}
```

### 💡 **Exemplo de uso no Bubble:**

O campo `file_base64` contém o arquivo completo em base64. No Bubble, você pode:

1. **Receber** o JSON da API
2. **Extrair** o campo `file_base64`  
3. **Converter** de base64 para arquivo no Bubble
4. **Usar** o arquivo normalmente

### 🎯 **API pronta para Postman e Bubble!**