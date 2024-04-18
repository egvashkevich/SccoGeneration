package ru.scco.pdf_generator;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

@Configuration
public class Config {
    @Value("${rabbit.pdf_generation_exchange}")
    private String exchangeName;


    @Bean
    DirectExchange exchange() {
        return new DirectExchange(exchangeName, true, false);
    }

    @Bean
    Queue inputQueue(@Value("${rabbit.pdf_generation_queue}") String name) {
        return new Queue(name, true);
    }

    @Bean
    Queue parseBotQueue(@Value("${rabbit.parser_bot_queue}") String name) {
        return new Queue(name, true);
    }

    @Bean
    Queue subscriberQueue(@Value("${rabbit.subscriber_queue}") String name) {
        return new Queue(name, true);
    }

    @Bean
    Binding bindingCP(Queue subscriberQueue, DirectExchange exchange,
                      @Value("${rabbit.file_link_key}") String key) {
        return BindingBuilder.bind(subscriberQueue).to(exchange).with(key);
    }

    @Bean
    Binding bindingError(Queue parseBotQueue, DirectExchange exchange,
                         @Value("${rabbit.error_key}") String key) {
        return BindingBuilder.bind(parseBotQueue).to(exchange).with(key);
    }

    @Bean
    Binding bindingOk(Queue parseBotQueue, DirectExchange exchange,
                      @Value("${rabbit.ok_key}") String key) {
        return BindingBuilder.bind(parseBotQueue).to(exchange).with(key);
    }

    @Bean
    public MessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(messageConverter());
        return rabbitTemplate;
    }

    @Bean
    PDFGenerator pdfGenerator(
            @Value("${pdf_generator.template}") String templatePath,
            @Value("${pdf_generator.font}") String fontPath,
            @Value("${pdf_generator.dest}") String destinationPath,
            @Value("${pdf_generator.fontsize}") int fontSize
            ) {
        return new PDFGenerator(templatePath, fontPath, destinationPath, fontSize);
    }

    @Bean
    ErrorsResponseMessages errorsMessages(
            @Value("${errors.file_error}") String fileError,
            @Value("${errors.db_error}") String dbError
    ) {
        return new ErrorsResponseMessages(fileError, dbError);
    }

    @Bean
    ExecutorService generatorPool() {
        return Executors.newFixedThreadPool(4);
    }
}
