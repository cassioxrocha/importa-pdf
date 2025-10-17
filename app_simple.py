"""
API Ultra Simples para PythonAnywhere + Bubble
Uma única chamada: detecta arquivo, move, retorna base64
"""

from flask import Flask, jsonify
import os
import shutil
import base64
from pathlib import Path

app = Flask(__name__)

# Configurações das pastas
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# Cria as pastas se não existirem
def ensure_folders():
    Path(INPUT_FOLDER).mkdir(exist_ok=True)
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    """Página inicial com informações da API."""
    return {
        'api': 'PDF Monitor for Bubble',
        'version': '1.0',
        'endpoints': {
            'GET /': 'Esta página',
            'GET /check': 'Verifica, move arquivo e retorna base64'
        },
        'status': 'online'
    }


@app.route('/check', methods=['GET'])
def check_and_process():
    """
    ÚNICA API NECESSÁRIA:
    1. Verifica se tem arquivo na pasta input
    2. Se sim: move para output e retorna base64
    3. Se não: retorna status vazio
    """
    try:
        ensure_folders()
        
        input_path = Path(INPUT_FOLDER)
        
        # Busca por qualquer arquivo na pasta input (PDF ou qualquer outro)
        files = [f for f in input_path.glob("*") if f.is_file()]
        
        if not files:
            return jsonify({
                'has_file': False,
                'status': 'no_files',
                'message': 'Nenhum arquivo encontrado'
            })
        
        # Pega o primeiro arquivo encontrado
        file_to_process = files[0]
        
        # Define destino na pasta output
        output_path = Path(OUTPUT_FOLDER) / file_to_process.name
        
        # Lê o conteúdo do arquivo
        with open(file_to_process, 'rb') as f:
            file_content = f.read()
        
        # Converte para base64
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # Move o arquivo
        shutil.move(str(file_to_process), str(output_path))
        
        # Retorna TUDO que o Bubble precisa
        return jsonify({
            'has_file': True,
            'status': 'success',
            'filename': file_to_process.name,
            'file_size': len(file_content),
            'file_base64': file_base64,
            'moved_to': f"output/{file_to_process.name}",
            'timestamp': str(Path(output_path).stat().st_mtime)
        })
        
    except Exception as e:
        return jsonify({
            'has_file': False,
            'status': 'error',
            'message': f'Erro: {str(e)}'
        }), 500


@app.route('/status', methods=['GET'])
def simple_status():
    """Status simples da API."""
    try:
        ensure_folders()
        input_path = Path(INPUT_FOLDER)
        files = [f for f in input_path.glob("*") if f.is_file()]
        
        return jsonify({
            'api_online': True,
            'files_waiting': len(files),
            'file_names': [f.name for f in files]
        })
        
    except Exception as e:
        return jsonify({
            'api_online': False,
            'error': str(e)
        }), 500


# Para PythonAnywhere
if __name__ == '__main__':
    # Desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Produção no PythonAnywhere
    ensure_folders()