package com.fccpd;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class TicketProducer {
    private static final String EXCHANGE_NAME = "ticket_exchange";
    private static final String ROUTING_KEY = "";
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm");

    public static void main(String[] args) throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        factory.setUsername("fccpd");
        factory.setPassword("fccpd123");
        factory.setVirtualHost("fccpd_vhost");

        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            
            // Declara a exchange do tipo fanout
            channel.exchangeDeclare(EXCHANGE_NAME, "fanout");

            Scanner scanner = new Scanner(System.in);
            System.out.println("Digite seu nome:");
            String producerName = scanner.nextLine();

            while (true) {
                System.out.println("\nDigite os detalhes do ingresso (ou 'sair' para encerrar):");
                System.out.println("Formato: evento,setor,preço");
                String input = scanner.nextLine();

                if ("sair".equalsIgnoreCase(input)) {
                    break;
                }

                String[] parts = input.split(",");
                if (parts.length != 3) {
                    System.out.println("Formato inválido! Use: evento,setor,preço");
                    continue;
                }

                String evento = parts[0].trim();
                String setor = parts[1].trim();
                String preco = parts[2].trim();

                String timestamp = LocalDateTime.now().format(DATE_FORMATTER);
                String message = String.format("[%s] %s : \"Ingresso para %s - %s - %s\"",
                        timestamp, producerName, evento, setor, preco);

                channel.basicPublish(EXCHANGE_NAME, ROUTING_KEY, null, message.getBytes());
                System.out.println("Mensagem enviada: " + message);
            }
        }
    }
} 