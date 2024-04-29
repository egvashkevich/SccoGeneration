package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import ru.scco.pdf_generator.dto.DBReplyDTO;
import ru.scco.pdf_generator.dto.DBRequestDTO;
import ru.scco.pdf_generator.dto.PDFCpResponseDTO;

//@Component
@RequiredArgsConstructor
public class Sender {
    private final RabbitTemplate template;
    private final String dbFunctionalExchange;
    private final String dbFunctionalRoutingKey;
    private final String outerExchange;
    private final String outerRoutingKey;

    public void sendCP(long userId, String fileLink) {
        template.convertAndSend(dbFunctionalExchange, dbFunctionalRoutingKey,
                                new DBRequestDTO(
                                        new PDFCpResponseDTO(userId, fileLink
                                        ), new DBReplyDTO(outerExchange,
                                                          outerRoutingKey)));
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
