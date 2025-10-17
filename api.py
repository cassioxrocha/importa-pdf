"""
API simples: verifica pasta, move arquivo, retorna conteúdo.
"""

from flask import Flask, jsonify, send_file, request
import os
import shutil
import base64
import threading
import time
import requests
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# Configurações das pastas
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# Cria as pastas se não existirem
Path(INPUT_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Lista para armazenar notificações
notifications = []
max_notifications = 50  # Máximo de notificações armazenadas

# Configurações de webhook
webhook_url = None  # URL do webhook a ser chamado
webhook_active = False


class PDFHandler(FileSystemEventHandler):
    """Handler para monitorar arquivos PDF."""
    
    def on_created(self, event):
        """Chamado quando um arquivo é criado."""
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            self.notify_pdf_added(event.src_path)
    
    def on_moved(self, event):
        """Chamado quando um arquivo é movido para a pasta."""
        if not event.is_directory and event.dest_path.lower().endswith('.pdf'):
            self.notify_pdf_added(event.dest_path)
    
    def notify_pdf_added(self, file_path):
        """Notifica que um PDF foi adicionado."""
        file_name = Path(file_path).name
        notification = {
            'timestamp': datetime.now().isoformat(),
            'event': 'pdf_added',
            'filename': file_name,
            'path': file_path,
            'message': f'📄 Novo PDF detectado: {file_name}'
        }
        
        # Adiciona à lista de notificações
        notifications.append(notification)
        
        # Mantém apenas as últimas notificações
        if len(notifications) > max_notifications:
            notifications.pop(0)
        
        print(f"🔔 ALERTA: {notification['message']}")
        
        # Envia webhook se configurado
        if webhook_active and webhook_url:
            self.send_webhook(notification)
    
    def send_webhook(self, notification):
        """Envia notificação via webhook."""
        try:
            # Payload para enviar ao Bubble
            payload = {
                'event': 'pdf_detected',
                'timestamp': notification['timestamp'],
                'filename': notification['filename'],
                'path': notification['path'],
                'message': notification['message'],
                'files_in_input': len(list(Path(INPUT_FOLDER).glob("*"))),
                'webhook_source': 'pdf_monitor_api'
            }
            
            # Envia POST para o webhook do Bubble
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"📡 Webhook enviado com sucesso para {webhook_url}")
            else:
                print(f"⚠️ Webhook falhou - Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro no webhook: {e}")


# Inicia o monitoramento
observer = None

def start_monitoring():
    """Inicia o monitoramento da pasta INPUT."""
    global observer
    
    if observer is None:
        event_handler = PDFHandler()
        observer = Observer()
        observer.schedule(event_handler, INPUT_FOLDER, recursive=False)
        observer.start()
        print(f"👀 Monitoramento ativo na pasta: {INPUT_FOLDER}/")

def stop_monitoring():
    """Para o monitoramento."""
    global observer
    
    if observer:
        observer.stop()
        observer.join()
        observer = None
        print("🛑 Monitoramento parado.")


@app.route('/process', methods=['GET'])
@app.route('/process/<filename>', methods=['GET'])
def process_file(filename=None):
    """
    Verifica se tem arquivo na pasta input.
    Se sim: move para output e retorna o conteúdo.
    Se não: retorna mensagem.
    
    Args:
        filename: Nome específico do arquivo para processar (opcional)
    """
    try:
        input_path = Path(INPUT_FOLDER)
        
        if filename:
            # Processa arquivo específico
            file_to_process = input_path / filename
            if not file_to_process.exists() or not file_to_process.is_file():
                return jsonify({
                    'status': 'file_not_found',
                    'message': f'Arquivo {filename} não encontrado na pasta input'
                }), 404
        else:
            # Busca por qualquer arquivo na pasta input
            files = list(input_path.glob("*"))
            files = [f for f in files if f.is_file()]  # Apenas arquivos, não pastas
            
            if not files:
                return jsonify({
                    'status': 'no_files',
                    'message': 'Nenhum arquivo encontrado na pasta input'
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
        
        # Retorna em formato JSON com base64
        return jsonify({
            'status': 'success',
            'filename': file_to_process.name,
            'file_size': len(file_content),
            'file_base64': file_base64,
            'moved_to': str(output_path)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro: {str(e)}'
        }), 500


@app.route('/status', methods=['GET'])
def check_status():
    """Verifica quantos arquivos tem na pasta input."""
    try:
        input_path = Path(INPUT_FOLDER)
        files = list(input_path.glob("*"))
        files = [f for f in files if f.is_file()]
        
        return jsonify({
            'status': 'ok',
            'files_in_input': len(files),
            'file_names': [f.name for f in files],
            'monitoring_active': observer is not None and observer.is_alive()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro: {str(e)}'
        }), 500


@app.route('/notifications', methods=['GET'])
def get_notifications():
    """Retorna todas as notificações de PDFs detectados."""
    return jsonify({
        'status': 'ok',
        'total_notifications': len(notifications),
        'notifications': notifications[-10:]  # Últimas 10 notificações
    })


@app.route('/notifications/latest', methods=['GET'])
def get_latest_notification():
    """Retorna apenas a última notificação."""
    if notifications:
        return jsonify({
            'status': 'new_notification',
            'notification': notifications[-1]
        })
    else:
        return jsonify({
            'status': 'no_notifications',
            'message': 'Nenhuma notificação ainda'
        })


@app.route('/notifications/clear', methods=['POST'])
def clear_notifications():
    """Limpa todas as notificações."""
    global notifications
    count = len(notifications)
    notifications.clear()
    
    return jsonify({
        'status': 'ok',
        'message': f'{count} notificações removidas'
    })


@app.route('/monitor/start', methods=['POST'])
def start_monitor():
    """Inicia o monitoramento."""
    try:
        start_monitoring()
        return jsonify({
            'status': 'ok',
            'message': 'Monitoramento iniciado'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar monitoramento: {str(e)}'
        }), 500


@app.route('/monitor/stop', methods=['POST'])
def stop_monitor():
    """Para o monitoramento."""
    try:
        stop_monitoring()
        return jsonify({
            'status': 'ok',
            'message': 'Monitoramento parado'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao parar monitoramento: {str(e)}'
        }), 500


@app.route('/webhook/configure', methods=['POST'])
def configure_webhook():
    """Configura a URL do webhook para notificações."""
    global webhook_url, webhook_active
    
    try:
        data = request.get_json()
        
        if not data or 'webhook_url' not in data:
            return jsonify({
                'status': 'error',
                'message': 'webhook_url é obrigatório no JSON'
            }), 400
        
        webhook_url = data['webhook_url']
        webhook_active = data.get('active', True)
        
        return jsonify({
            'status': 'ok',
            'message': 'Webhook configurado com sucesso',
            'webhook_url': webhook_url,
            'webhook_active': webhook_active
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao configurar webhook: {str(e)}'
        }), 500


@app.route('/webhook/status', methods=['GET'])
def webhook_status():
    """Retorna o status do webhook."""
    return jsonify({
        'webhook_configured': webhook_url is not None,
        'webhook_url': webhook_url,
        'webhook_active': webhook_active
    })


@app.route('/webhook/test', methods=['POST'])
def test_webhook():
    """Testa o webhook enviando uma notificação de teste."""
    if not webhook_active or not webhook_url:
        return jsonify({
            'status': 'error',
            'message': 'Webhook não está configurado ou não está ativo'
        }), 400
    
    try:
        test_payload = {
            'event': 'test_webhook',
            'timestamp': datetime.now().isoformat(),
            'filename': 'teste.pdf',
            'path': 'input/teste.pdf',
            'message': '🧪 Teste de webhook - API funcionando',
            'files_in_input': 0,
            'webhook_source': 'pdf_monitor_api'
        }
        
        response = requests.post(
            webhook_url,
            json=test_payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify({
            'status': 'ok',
            'message': 'Webhook de teste enviado',
            'response_status': response.status_code,
            'webhook_url': webhook_url
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro no teste do webhook: {str(e)}'
        }), 500


@app.route('/webhook/disable', methods=['POST'])
def disable_webhook():
    """Desativa o webhook."""
    global webhook_active
    webhook_active = False
    
    return jsonify({
        'status': 'ok',
        'message': 'Webhook desativado'
    })


if __name__ == '__main__':
    print("🚀 API com Monitor - Move arquivos e monitora pasta")
    print("📁 Pastas:")
    print(f"   Input:  {INPUT_FOLDER}/")
    print(f"   Output: {OUTPUT_FOLDER}/")
    print("🌐 Endpoints:")
    print("   GET /status                - Verifica arquivos e status do monitor")
    print("   GET /process               - Move arquivo e retorna conteúdo em base64")
    print("   GET /notifications         - Lista notificações de PDFs detectados")
    print("   GET /notifications/latest  - Última notificação")
    print("   POST /notifications/clear  - Limpa notificações")
    print("   POST /monitor/start        - Inicia monitoramento")
    print("   POST /monitor/stop         - Para monitoramento")
    print("   POST /webhook/configure    - Configura webhook do Bubble")
    print("   GET /webhook/status        - Status do webhook")
    print("   POST /webhook/test         - Testa webhook")
    print("   POST /webhook/disable      - Desativa webhook")
    print("🔗 Acesse: http://localhost:5000")
    
    try:
        # Inicia monitoramento automaticamente
        start_monitoring()
        
        # Inicia Flask
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n🛑 Parando aplicação...")
        stop_monitoring()
    except Exception as e:
        print(f"❌ Erro: {e}")
        stop_monitoring()