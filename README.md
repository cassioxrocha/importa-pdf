# API Simples - Move Arquivos

API REST **ultra simples** que:
1. ✅ Verifica se tem arquivo na pasta `input/`
2. ✅ Move o arquivo para pasta `output/`  
3. ✅ Retorna o conteúdo do arquivo em **base64** (compatível com Bubble)

## � Como usar

### 1. Instalar dependências:
```bash
pip install Flask
```

### 2. Iniciar a API:
```bash
python api.py
```

### 3. Usar os endpoints:

**Verificar status:**
```bash
curl http://localhost:5000/status
```

**Processar arquivo:**
```bash
curl http://localhost:5000/process
```

## 📡 Endpoints

| URL | Descrição |
|-----|-----------|
| `GET /status` | Mostra quantos arquivos tem na pasta input |
| `GET /process` | Move primeiro arquivo para output e retorna conteúdo em **base64** |

## 📁 Estrutura

```
input/     # Coloque arquivos aqui
output/    # Arquivos processados vão para aqui
api.py     # Código da API
```

## � Exemplo

1. Coloque um arquivo em `input/`
2. Acesse: `http://localhost:5000/process`
3. O arquivo será movido para `output/` e baixado automaticamente

**Pronto! Só isso mesmo. API simples e direta.** 🎯
