package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;
import ru.scco.pdf_generator.dto.PDFCpResponseDTO;
import ru.scco.pdf_generator.dto.PDFStatusResponseDTO;

//@Component
@RequiredArgsConstructor
public class Sender {
    private final RabbitTemplate template;
    private final String dbFunctionalExchange;
    private final String dbFunctionalRoutingKey;

    public void sendCP(long userId, String fileLink) {
        template.convertAndSend(dbFunctionalExchange, dbFunctionalRoutingKey,
                                new PDFCpResponseDTO(userId, fileLink));
    }

    public void sendOk(long userId) {
        // Пока никуда
//        template.convertAndSend(dbFunctionalExchange, dbFunctionalRoutingKey,
//                                new PDFStatusResponseDTO(userId, true, null));
    }

    public void sendError(long userId,
                          String errorMessage) {
        // Пока никуда
//        template.convertAndSend(dbFunctionalExchange,
//                                dbFunctionalRoutingKey,
//                                new PDFStatusResponseDTO(userId, false,
//                                                         errorMessage));
    }
}
