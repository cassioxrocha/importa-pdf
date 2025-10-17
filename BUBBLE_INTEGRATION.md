# Integração com Bubble.io

Este documento descreve como integrar a API de importação de PDFs com a plataforma Bubble.io.

## Passo 1: Configurar a API no Bubble

1. No seu aplicativo Bubble, vá para **Plugins** → **API Connector**
2. Se não tiver o plugin instalado, adicione o **API Connector** plugin
3. Clique em **Add another API**
4. Configure a API:
   - **API Name**: PDF Import API
   - **Authentication**: None (ou configure se você adicionar autenticação)

## Passo 2: Configurar o Endpoint GET PDF

1. Adicione uma nova **API Call** chamada "Get PDF"
2. Configure:
   - **Use as**: Action
   - **Data type**: File
   - **Method**: GET
   - **URL**: `http://seu-servidor.com:8000/get-pdf`

### Exemplo de URL:
```
http://192.168.1.100:8000/get-pdf
```

Se você estiver usando HTTPS com domínio:
```
https://api.seudominio.com/get-pdf
```

## Passo 3: Configurar o Endpoint de Verificação (Opcional)

Para verificar se existe um PDF antes de baixá-lo:

1. Adicione outra **API Call** chamada "Check PDF"
2. Configure:
   - **Use as**: Data
   - **Data type**: JSON
   - **Method**: GET
   - **URL**: `http://seu-servidor.com:8000/check-pdf`

### Estrutura de Resposta:
```json
{
  "found": true,
  "filename": "documento.pdf",
  "size_bytes": 102400,
  "path": "/caminho/completo/documento.pdf"
}
```

## Passo 4: Usar a API em Workflows do Bubble

### Exemplo 1: Baixar PDF quando usuário clica em um botão

1. Crie um botão no seu app
2. Adicione um **Workflow** ao evento de clique
3. Adicione uma ação: **Plugins** → **PDF Import API - Get PDF**
4. Use o resultado para:
   - Mostrar o PDF ao usuário
   - Salvar em um campo de tipo file do Bubble
   - Enviar por email
   - Upload para outro serviço

### Exemplo 2: Verificar e depois baixar

**Workflow Step 1:**
```
When Button is clicked
→ Call API: Check PDF
```

**Workflow Step 2:**
```
Only when: Result of Step 1's found is "yes"
→ Call API: Get PDF
```

## Passo 5: Tratamento de Erros

A API retorna erro 404 quando não há PDF disponível. No Bubble:

1. Configure um **Custom State** para armazenar o status
2. Use **Conditional** para mostrar mensagens apropriadas:
   - Se sucesso: "PDF baixado com sucesso!"
   - Se erro 404: "Nenhum PDF disponível no momento"

### Exemplo de Conditional:
```
When PDF Import API's Get PDF:status code is 404
→ Show element "No PDF Available Message"
```

## Exemplos de Uso Práticos

### Caso de Uso 1: Sistema de Importação de Faturas
1. PDFs de faturas são colocados na pasta do servidor
2. Bubble verifica periodicamente se há novos PDFs
3. Quando encontrado, o PDF é baixado e processado
4. Dados são extraídos e salvos no banco de dados

### Caso de Uso 2: Fila de Documentos
1. Múltiplos PDFs são adicionados à pasta
2. Bubble chama a API repetidamente
3. Cada chamada retorna e remove um PDF
4. Processo continua até não haver mais PDFs

### Caso de Uso 3: Integração com Scanner
1. Scanner salva PDFs diretamente na pasta monitorada
2. Bubble agenda workflow para verificar novos PDFs a cada X minutos
3. Quando encontrado, PDF é importado e processado automaticamente

## Configuração de Agendamento no Bubble

Para verificar periodicamente por novos PDFs:

1. Vá para **Backend workflows**
2. Crie um **Recurring Event**
3. Configure:
   - **Interval**: A cada 5 minutos (ou conforme necessário)
   - **Action**: Call API Check PDF
   - **Conditional**: Se found = yes, então call Get PDF

## Dicas e Boas Práticas

1. **Timeout**: Configure um timeout apropriado na chamada da API (pelo menos 30 segundos)
2. **Retry**: Configure retry logic caso a API esteja temporariamente indisponível
3. **Logs**: Ative logging no Bubble para debug
4. **Testes**: Use o endpoint `/check-pdf` para testes sem deletar arquivos
5. **Backup**: Considere fazer backup dos PDFs antes de deletá-los

## Troubleshooting

### Problema: API não responde
**Solução**: Verifique se o servidor está rodando e se a porta está acessível

### Problema: Erro de CORS
**Solução**: Se chamar a API do navegador, adicione configuração de CORS no servidor

### Problema: PDF não é deletado
**Solução**: Verifique as permissões da pasta no servidor

### Problema: 404 quando há PDF na pasta
**Solução**: 
- Verifique se o caminho da pasta está correto
- Confirme que os arquivos têm extensão `.pdf`
- Verifique permissões de leitura da pasta

## Suporte

Para mais informações sobre a API, consulte o README.md principal ou acesse:
- Documentação interativa: `http://seu-servidor:8000/docs`
- Health check: `http://seu-servidor:8000/health`
