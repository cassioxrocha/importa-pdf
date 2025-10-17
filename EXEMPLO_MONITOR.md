# 🔔 EXEMPLO: API com Monitoramento de PDFs

## ✅ **API funcionando com monitoramento ativo!**

### 🎯 **Como testar no Postman:**

1. **Verificar status:**
   ```
   GET http://localhost:5000/status
   ```
   Response: `"monitoring_active": true`

2. **Ver última notificação:**
   ```
   GET http://localhost:5000/notifications/latest
   ```

3. **TESTE AO VIVO:** 
   - Copie um PDF para a pasta `input/`
   - Imediatamente chame: `GET /notifications/latest`
   - Verá a notificação do PDF detectado!

4. **Processar arquivo:**
   ```
   GET http://localhost:5000/process
   ```
   Retorna arquivo em base64 + move para output

## 🔄 **Monitoramento Automático:**

- ✅ **Detecta PDFs** instantaneamente quando copiados
- ✅ **Gera notificações** com timestamp  
- ✅ **Armazena histórico** das últimas 50 notificações
- ✅ **Ideal para integração** com Bubble via polling

## 📡 **Endpoints principais:**

| Endpoint | Descrição |
|----------|-----------|
| `/status` | Status da pasta + monitoramento |
| `/process` | Move arquivo e retorna base64 |
| `/notifications/latest` | **Polling** - última notificação |
| `/notifications` | Histórico completo |

**🎉 Pronto para usar! Coloque um PDF na pasta `input/` e veja a mágica acontecer!**