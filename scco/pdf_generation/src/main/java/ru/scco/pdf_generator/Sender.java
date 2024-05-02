package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;
import ru.scco.pdf_generator.dto.*;

@Component
@RequiredArgsConstructor
public class Sender {
    private final RabbitTemplate template;
    private final Binding crudResponseBinding;
    private final Binding dbBinding;
    private final Binding outerBinding;
//    private final String dbFunctionalExchange;
//    private final String dbFunctionalRoutingKey;
//
//    private final String outerExchange;
//    private final String outerRoutingKey;

    public void sendCPToDB(long messageID, String fileLink) {
        template.convertAndSend(dbBinding.getExchange(),
                                dbBinding.getRoutingKey(),
                                new DBRequestDTO(
                                        new DBInsertRequestData(messageID,
                                                                fileLink
                                        ), new DBReplyDTO(
                                        crudResponseBinding.getExchange(),
                                        crudResponseBinding.getRoutingKey())));
    }

    public void sendCPToOutput(long customerID, long clientID,
                               String fileLink) {
        template.convertAndSend(outerBinding.getExchange(),
                                outerBinding.getRoutingKey(),
                                new PDFResponseDTO(customerID, clientID,
                                                   fileLink));
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
