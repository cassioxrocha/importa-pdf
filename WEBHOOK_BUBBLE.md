# 🔔 WEBHOOK para BUBBLE - Configuração

## 🎯 **Como funciona:**

1. **Bubble cria** um endpoint webhook
2. **API configura** a URL do webhook do Bubble
3. **Quando PDF é adicionado** → API envia notificação automática para o Bubble
4. **Bubble recebe** dados instantaneamente (sem polling!)

## 📡 **Configurando no Postman:**

### 1. **Configurar webhook:**
```
POST http://localhost:5000/webhook/configure
Content-Type: application/json

{
  "webhook_url": "https://seu-app.bubbleapps.io/api/1.1/wf/pdf-detected",
  "active": true
}
```

### 2. **Verificar status:**
```
GET http://localhost:5000/webhook/status
```

### 3. **Testar webhook:**
```
POST http://localhost:5000/webhook/test
```

## 🔄 **Fluxo completo:**

1. **Configure o webhook** com URL do Bubble
2. **Coloque PDF** na pasta `input/`
3. **API detecta** automaticamente
4. **Webhook enviado** para Bubble com dados:

```json
{
  "event": "pdf_detected",
  "timestamp": "2025-10-17T10:30:15.123456",
  "filename": "documento.pdf",
  "path": "input/documento.pdf",
  "message": "📄 Novo PDF detectado: documento.pdf",
  "files_in_input": 1,
  "webhook_source": "pdf_monitor_api"
}
```

5. **Bubble processa** automaticamente
6. **Bubble chama** `/process` para obter arquivo em base64

## 🎯 **Vantagens do Webhook:**

- ✅ **Tempo real** - Sem delay de polling
- ✅ **Eficiente** - Só envia quando necessário  
- ✅ **Confiável** - Retries automáticos
- ✅ **Simples** - Um endpoint no Bubble recebe tudo

## 🔧 **No Bubble:**

1. Crie **API Workflow** endpoint
2. Configure para receber **POST** com dados JSON
3. **URL exemplo:** `https://seu-app.bubbleapps.io/api/1.1/wf/pdf-detected`
4. Configure na API usando `/webhook/configure`

**Agora o Bubble recebe notificações automáticas! 🎉**