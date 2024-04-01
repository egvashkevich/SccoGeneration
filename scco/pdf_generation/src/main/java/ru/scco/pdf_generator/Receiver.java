package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import ru.scco.pdf_generator.dto.PDFGeneratorRequestDTO;

import java.util.concurrent.ExecutorService;

@Slf4j
@Service
@RequiredArgsConstructor
public class Receiver {
    private final PDFGenerator pdfGenerator;
    private final DBManager manager;
    private final Sender sender;
    private final ErrorsResponseMessages errorsMessages;
    private final ExecutorService generatorPool;

    @RabbitListener(queues = {"${rabbit.pdf_generation_queue}"}, concurrency
            = "1")
    public void consume(PDFGeneratorRequestDTO request) {
        generatorPool.execute(() -> {
            String fileLink = pdfGenerator.generate(request.queryId(),
                                                    request.senderId(),
                                                    request.cp(),
                                                    request.signature());
            if (fileLink == null) {
                sender.sendError(request.senderId(),
                                 errorsMessages.fileError());
            }
            if (manager.saveCP(request.senderId(), fileLink)) {
                sender.sendCP(request.senderId(), fileLink);
                sender.sendOk(request.senderId());
            } else {
                sender.sendError(request.senderId(), errorsMessages.dbError());
            }
        });

    }

}