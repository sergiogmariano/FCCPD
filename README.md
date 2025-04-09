# Sistema de Troca de Ingressos com RabbitMQ

Este projeto implementa um sistema de troca de ingressos utilizando RabbitMQ como intermediário de mensagens.

## Estrutura do Projeto

- `producer/`: Produtor de mensagens em Java
- `consumer/`: Consumidor de mensagens em Python
- `audit/`: Backend de auditoria em Python

## Requisitos

- Java 11 ou superior
- Python 3.8 ou superior
- RabbitMQ Server
- Maven (para o projeto Java)
- pip (para os projetos Python)

## Configuração do RabbitMQ

1. Instalar o RabbitMQ Server
2. Criar um usuário e vhost:
   ```bash
   rabbitmqctl add_user fccpd fccpd123
   rabbitmqctl add_vhost fccpd_vhost
   rabbitmqctl set_user_tags fccpd administrator
   rabbitmqctl set_permissions -p fccpd_vhost fccpd ".*" ".*" ".*"
   ```

## Instalação

### Produtor (Java)
```bash
cd producer
mvn clean install
```

### Consumidor (Python)
```bash
cd consumer
pip install -r requirements.txt
```

### Auditoria (Python)
```bash
cd audit
pip install -r requirements.txt
```

## Execução

1. Iniciar o RabbitMQ Server
2. Iniciar o backend de auditoria:
   ```bash
   cd audit
   python main.py
   ```
3. Iniciar o consumidor:
   ```bash
   cd consumer
   python main.py
   ```
4. Iniciar o produtor:
   ```bash
   cd producer
   mvn exec:java
   ``` 
