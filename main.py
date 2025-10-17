"""
API para importar e retornar arquivos PDF de uma pasta.
Esta API é projetada para ser chamada pelo Bubble.
"""
import os
import glob
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uvicorn


# Configuração
PDF_FOLDER_PATH = os.getenv("PDF_FOLDER_PATH", "./pdfs")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Criar aplicação FastAPI
app = FastAPI(
    title="PDF Import API",
    description="API para verificar, retornar e apagar arquivos PDF de uma pasta",
    version="1.0.0"
)


def get_first_pdf() -> Optional[Path]:
    """
    Procura o primeiro arquivo PDF na pasta configurada.
    
    Returns:
        Path do arquivo PDF ou None se não encontrar nenhum
    """
    pdf_folder = Path(PDF_FOLDER_PATH)
    
    # Criar pasta se não existir
    pdf_folder.mkdir(parents=True, exist_ok=True)
    
    # Procurar arquivos PDF
    pdf_files = list(pdf_folder.glob("*.pdf"))
    
    if pdf_files:
        # Retornar o primeiro PDF encontrado
        return pdf_files[0]
    
    return None


@app.get("/")
def root():
    """Endpoint raiz com informações da API"""
    return {
        "api": "PDF Import API",
        "version": "1.0.0",
        "description": "Use /get-pdf para obter e apagar um PDF da pasta"
    }


@app.get("/get-pdf")
async def get_pdf():
    """
    Endpoint principal que verifica se existe um PDF na pasta.
    Se existir, retorna o arquivo e o apaga da pasta.
    
    Returns:
        FileResponse com o PDF ou erro 404 se não encontrar nenhum PDF
    """
    pdf_file = get_first_pdf()
    
    if pdf_file is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhum arquivo PDF encontrado na pasta"
        )
    
    pdf_path = pdf_file.absolute()
    filename = pdf_file.name
    
    # Criar resposta com o arquivo
    response = FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
    
    # Registrar callback para apagar o arquivo após enviar
    response.background = BackgroundTask(delete_file, pdf_path)
    
    return response


@app.get("/check-pdf")
def check_pdf():
    """
    Endpoint para verificar se existe um PDF na pasta sem deletá-lo.
    Útil para testes e verificação.
    
    Returns:
        JSON com informações sobre o PDF encontrado ou mensagem de não encontrado
    """
    pdf_file = get_first_pdf()
    
    if pdf_file is None:
        return JSONResponse(
            status_code=200,
            content={
                "found": False,
                "message": "Nenhum arquivo PDF encontrado na pasta"
            }
        )
    
    return {
        "found": True,
        "filename": pdf_file.name,
        "size_bytes": pdf_file.stat().st_size,
        "path": str(pdf_file.absolute())
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}


def delete_file(file_path: Path):
    """
    Apaga o arquivo do sistema de arquivos.
    
    Args:
        file_path: Path do arquivo a ser apagado
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo {file_path} apagado com sucesso")
    except Exception as e:
        print(f"Erro ao apagar arquivo {file_path}: {e}")


# Importar BackgroundTask após definir a função
from fastapi import BackgroundTasks
from starlette.background import BackgroundTask


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
