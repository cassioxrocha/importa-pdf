# 🔧 TESTE DA API SIMPLIFICADA - BUBBLE + PYTHONANYWHERE

## 🏠 **API Local (para testar antes do deploy):**

### Rodar local:
```bash
python app_simple.py
```
**URL Local:** `http://localhost:5000`

---

## 🌐 **API Online (PythonAnywhere):**
**URL Online:** `https://seuusuario.pythonanywhere.com`

---

## 🧪 **Testes no Postman:**

### **1. Status da API**
```
GET /status
```
**Response:**
```json
{
  "status": "API Online",
  "version": "Simple v1.0",
  "input_folder": "Exists",
  "output_folder": "Exists"
}
```

### **2. Verificar/Processar arquivo**
```
GET /check
```

**Cenário 1 - SEM arquivos:**
```json
{
  "has_file": false,
  "status": "no_files", 
  "message": "Nenhum arquivo encontrado"
}
```

**Cenário 2 - COM arquivo:**
```json
{
  "has_file": true,
  "status": "success",
  "filename": "teste.pdf",
  "file_size": 2048,
  "file_base64": "JVBERi0xLjQKJcOkw7zDssOgCj...",
  "moved_to": "output/teste.pdf"
}
```

---

## 🎯 **Bubble - Data API Connector:**

### **Setup:**
1. **Name:** PDF Processor
2. **Authentication:** None
3. **Shared headers:** Nenhum

### **Call: Check for PDF**
- **Use as:** Action
- **Data type:** JSON
- **URL:** `https://seuusuario.pythonanywhere.com/check`
- **Method:** GET
- **Body type:** None

### **Response Fields:**
```
has_file: boolean
status: text  
filename: text
file_size: number
file_base64: text
moved_to: text
message: text
```

---

## 🔄 **Bubble Workflow Completo:**

### **Schedule API Workflow** (30s):
```
1. Call: PDF Processor - Check for PDF

2. When Result has_file = yes:
   - Save file_base64 to Thing
   - Create File from base64
   - Process PDF content
   - Show notification "Arquivo processado!"

3. When Result has_file = no:
   - Do nothing (aguarda próxima verificação)
```

### **Manual Button Test:**
```
When Button "Test PDF" is clicked:
1. Call: PDF Processor - Check for PDF
2. Show Result's file_base64 in Text element
```

---

## 📁 **Estrutura de pastas:**

```
/home/seuusuario/mysite/
├── app_simple.py          # API Flask
├── requirements_simple.txt # Dependências
├── input/                 # PDFs para processar
├── output/               # PDFs processados
└── DEPLOY_PYTHONANYWHERE.md
```

---

## ✅ **Checklist de Deploy:**

- [ ] Upload `app_simple.py`
- [ ] Upload `requirements_simple.txt` 
- [ ] Instalar Flask: `pip3.10 install --user flask`
- [ ] Configurar WSGI file
- [ ] Criar pastas `input/` e `output/`
- [ ] Testar `/status`
- [ ] Testar `/check` vazio
- [ ] Upload PDF teste
- [ ] Testar `/check` com arquivo
- [ ] Configurar Bubble API Connector
- [ ] Testar workflow manual
- [ ] Configurar schedule workflow

## 🎉 **API pronta para produção! 🚀**