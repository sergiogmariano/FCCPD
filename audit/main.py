import pika
import json
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import queue

app = Flask(__name__)
CORS(app)

# Fila para armazenar as mensagens
message_queue = queue.Queue()

# Configurações do RabbitMQ
EXCHANGE_NAME = 'ticket_exchange'
AUDIT_QUEUE_NAME = 'audit_queue'
ROUTING_KEY = ''

def callback(ch, method, properties, body):
    """Callback para processar mensagens recebidas"""
    message = body.decode()
    message_queue.put(message)

def consume_messages():
    """Função para consumir mensagens do RabbitMQ"""
    credentials = pika.PlainCredentials('fccpd', 'fccpd123')
    parameters = pika.ConnectionParameters(
        'localhost',
        5672,
        'fccpd_vhost',
        credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declara a exchange
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout'
    )

    # Declara a fila de auditoria
    channel.queue_declare(
        queue=AUDIT_QUEUE_NAME,
        durable=True
    )

    # Vincula a fila à exchange
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=AUDIT_QUEUE_NAME,
        routing_key=ROUTING_KEY
    )

    print(' [*] Aguardando mensagens para auditoria. Para sair pressione CTRL+C')
    
    channel.basic_consume(
        queue=AUDIT_QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

@app.route('/messages', methods=['GET'])
def get_messages():
    """Endpoint para obter todas as mensagens recebidas"""
    messages = []
    while not message_queue.empty():
        messages.append(message_queue.get())
    return jsonify(messages)

if __name__ == '__main__':
    # Inicia o consumidor em uma thread separada
    consumer_thread = Thread(target=consume_messages, daemon=True)
    consumer_thread.start()

    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000) 