# 🚀 DEPLOY NO PYTHONANYWHERE - GUIA COMPLETO

## 📁 **Arquivos para upload:**
- `app_simple.py` (API simplificada)
- `requirements_simple.txt` (apenas Flask)

## 🔧 **Passos no PythonAnywhere:**

### 1. **Upload dos arquivos:**
- Acesse: Files → Upload
- Envie `app_simple.py` e `requirements_simple.txt`
- Coloque na pasta `/home/seuusuario/mysite/`

### 2. **Instalar dependências:**
```bash
# No console Bash do PythonAnywhere:
cd ~/mysite
pip3.10 install --user -r requirements_simple.txt
```

### 3. **Configurar Web App:**
- Web → Create a new web app
- Escolha Flask
- Python 3.10
- Source code: `/home/seuusuario/mysite/`
- WSGI file: edite para:

```python
import sys
import os

# Adicionar o diretório do projeto ao Python path
path = '/home/seuusuario/mysite'
if path not in sys.path:
    sys.path.append(path)

# Importar a aplicação Flask
from app_simple import app as application

if __name__ == "__main__":
    application.run()
```

### 4. **Criar pastas:**
No Files do PythonAnywhere:
- Criar pasta `input/` em `/home/seuusuario/mysite/`
- Criar pasta `output/` em `/home/seuusuario/mysite/`

## 🌐 **URLs da API online:**

Sua API ficará em:
- **Home:** `https://seuusuario.pythonanywhere.com/`
- **Check:** `https://seuusuario.pythonanywhere.com/check`
- **Status:** `https://seuusuario.pythonanywhere.com/status`

## 🎯 **Como o Bubble vai usar:**

### **Chamada única no Bubble:**
```
GET https://seuusuario.pythonanywhere.com/check
```

### **Response quando tem arquivo:**
```json
{
  "has_file": true,
  "status": "success",
  "filename": "documento.pdf",
  "file_size": 1024,
  "file_base64": "JVBERi0xLjQK...",
  "moved_to": "output/documento.pdf"
}
```

### **Response quando não tem arquivo:**
```json
{
  "has_file": false,
  "status": "no_files",
  "message": "Nenhum arquivo encontrado"
}
```

## 🔄 **Fluxo no Bubble:**

1. **Schedule API Workflow** (a cada 30 segundos)
2. **Chama:** `GET /check`
3. **Se** `has_file = true` → **Processa** `file_base64`
4. **Se** `has_file = false` → **Aguarda** próxima verificação

## 📤 **Como adicionar arquivos:**

### Via PythonAnywhere Files:
1. Files → `/home/seuusuario/mysite/input/`
2. Upload do PDF
3. Bubble detecta na próxima chamada

### Via FTP/SFTP:
- Host: `seuusuario.pythonanywhere.com`
- User: `seuusuario`
- Pasta: `/home/seuusuario/mysite/input/`

## ✅ **Vantagens desta versão:**

- ✅ **Uma única API** - `/check` faz tudo
- ✅ **Sem webhook** - Bubble faz polling simples
- ✅ **Mínimas dependências** - Só Flask
- ✅ **Deploy fácil** - PythonAnywhere gratuito
- ✅ **Sem monitoramento** - Menos complexidade
- ✅ **Funciona offline** - Não precisa de internet constante

## 🎯 **API pronta para PythonAnywhere + Bubble! 🚀**