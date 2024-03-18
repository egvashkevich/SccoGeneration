package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import ru.scco.pdf_generator.dto.PDFGeneratorRequestDTO;

@Slf4j
@Service
@RequiredArgsConstructor
public class Receiver {
    private final DBManager manager;
    private final Sender sender;

    @RabbitListener(queues = {"${rabbit.pdf_generation_queue}"})
    public void consume(PDFGeneratorRequestDTO request) {
        System.out.println(request.senderId() + " " + request.cp());
        String fileLink = PDFGenerator.generate(request.senderId(),
                                                request.cp());
        if (manager.saveCP(request.senderId(), fileLink)) {
            sender.sendCP(request.senderId(), fileLink);
            sender.sendOk(request.senderId());
        }
    }
}
