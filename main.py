from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

# --- LISTA DOS SEUS ROBÔS ---
# Coloque aqui o endereço COMPLETO dos seus bots que estão no Easypanel
# Não esqueça do /webhook no final de cada um!
BOTS = [
    "https://bot-empresa-1.seu-dominio.easypanel.host/webhook",
    "https://bot-empresa-2.seu-dominio.easypanel.host/webhook"
]

def encaminhar_mensagem(url, json_data):
    """Envia a mensagem para um bot sem travar o processo"""
    try:
        requests.post(url, json=json_data, timeout=5)
    except Exception as e:
        print(f"❌ Falha ao enviar para {url}: {e}")

@app.route('/webhook', methods=['POST'])
def receber_webhook():
    data = request.json
    
    # Recebe a mensagem da Evolution e espalha para todos os bots
    print(f"📨 Nova mensagem recebida! Espalhando para {len(BOTS)} robôs...")
    
    for bot_url in BOTS:
        # Usa threading para disparar rápido e não deixar a Evolution esperando
        t = threading.Thread(target=encaminhar_mensagem, args=(bot_url, data))
        t.start()
        
    # Responde OK para a Evolution imediatamente
    return jsonify({"status": "encaminhado"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)