import pika
import sys
import time

# Configurações do RabbitMQ
EXCHANGE_NAME = 'ticket_exchange'
QUEUE_NAME = 'ticket_queue'
ROUTING_KEY = ''

def callback(ch, method, properties, body):
    print(f" [x] Recebido: {body.decode()}")

def main():
    # Configuração da conexão
    credentials = pika.PlainCredentials('fccpd', 'fccpd123')
    parameters = pika.ConnectionParameters(
        'localhost',
        5672,
        'fccpd_vhost',
        credentials
    )

    try:
        # Estabelece conexão
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declara a exchange
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='fanout'
        )

        # Declara a fila
        result = channel.queue_declare(
            queue=QUEUE_NAME,
            exclusive=True
        )

        # Vincula a fila à exchange
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key=ROUTING_KEY
        )

        print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
        
        # Inicia o consumo
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()

    except KeyboardInterrupt:
        print(' Interrompido')
        sys.exit(0)
    except Exception as e:
        print(f' Erro: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main() 