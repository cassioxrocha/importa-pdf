# 🧪 TESTANDO WEBHOOK NO POSTMAN

## 📡 **1. Configurar Webhook:**

### Request:
```
POST http://localhost:5000/webhook/configure
Content-Type: application/json

Body (raw JSON):
{
  "webhook_url": "https://httpbin.org/post",
  "active": true
}
```

### Response esperado:
```json
{
  "status": "ok",
  "message": "Webhook configurado com sucesso",
  "webhook_url": "https://httpbin.org/post",
  "webhook_active": true
}
```

---

## ✅ **2. Verificar Status do Webhook:**

### Request:
```
GET http://localhost:5000/webhook/status
```

### Response esperado:
```json
{
  "webhook_configured": true,
  "webhook_url": "https://httpbin.org/post", 
  "webhook_active": true
}
```

---

## 🧪 **3. Testar Webhook (Envio Manual):**

### Request:
```
POST http://localhost:5000/webhook/test
```

### Response esperado:
```json
{
  "status": "ok",
  "message": "Webhook de teste enviado",
  "response_status": 200,
  "webhook_url": "https://httpbin.org/post"
}
```

### 🎯 **O que acontece:**
- API envia POST para `https://httpbin.org/post`
- httpbin.org recebe e mostra os dados
- Você pode ver no httpbin.org que recebeu o JSON

---

## 🔄 **4. Simular Detecção de PDF:**

### Passos:
1. **Configure webhook** (passo 1)
2. **Coloque um PDF** na pasta `input/`
3. **API detecta automaticamente** 
4. **Webhook é disparado** para URL configurada
5. **Veja no console da API** a mensagem: `📡 Webhook enviado com sucesso`

---

## 🌐 **URLs de teste gratuitas:**

### **httpbin.org** (recomendado):
```
https://httpbin.org/post
```
- Recebe qualquer POST
- Mostra dados recebidos
- Perfeito para testes

### **webhook.site**:
1. Acesse: https://webhook.site
2. Copie a URL única gerada
3. Use como webhook_url

### **RequestBin**:
1. Acesse: https://requestbin.com
2. Crie um bin temporário  
3. Use a URL gerada

---

## 📝 **Exemplo completo no Postman:**

### Collection para testar:

1. **POST** `/webhook/configure` 
   - Body: `{"webhook_url": "https://httpbin.org/post", "active": true}`

2. **GET** `/webhook/status`
   - Verifica se configurou

3. **POST** `/webhook/test` 
   - Envia teste manual

4. **Adicionar PDF na pasta** `input/`
   - Webhook automático disparado

5. **GET** `/notifications/latest`
   - Vê última notificação gerada

---

## ✅ **Como saber se funcionou:**

- ✅ **Console da API** mostra: `📡 Webhook enviado com sucesso`
- ✅ **httpbin.org** mostra dados JSON recebidos
- ✅ **Status 200** no response do `/webhook/test`

**Pronto para testar no Postman! 🎯**