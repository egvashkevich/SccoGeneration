package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;
import ru.scco.pdf_generator.dto.PDFCpResponseDTO;
import ru.scco.pdf_generator.dto.PDFStatusResponseDTO;

@Component
@RequiredArgsConstructor
public class Sender {
    private final RabbitTemplate template;
    private final DirectExchange exchange;
    private final Binding bindingCP;
    private final Binding bindingOk;
    private final Binding bindingError;

    public void sendCP(long userId, String fileLink) {
        template.convertAndSend(exchange.getName(), bindingCP.getRoutingKey(),
                                new PDFCpResponseDTO(userId, fileLink));
    }

    public void sendOk(long userId) {
        template.convertAndSend(exchange.getName(), bindingOk.getRoutingKey(),
                                new PDFStatusResponseDTO(userId, true, null));
    }

    public void sendError(long userId,
                          String errorMessage) {
        template.convertAndSend(exchange.getName(),
                                bindingError.getRoutingKey(),
                                new PDFStatusResponseDTO(userId, false,
                                                         errorMessage));
    }
}
