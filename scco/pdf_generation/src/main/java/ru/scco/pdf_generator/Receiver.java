package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import ru.scco.pdf_generator.dto.PDFGeneratorRequestDTO;
import ru.scco.pdf_generator.processors.ProcessingChain;

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
    private final ProcessingChain processingChain;

    @RabbitListener(queues = {"${rabbit.pdf_generation_queue}"})
    public void consume(PDFGeneratorRequestDTO request) {
        generatorPool.execute(() -> {
            String cp;
            try {
                cp = processingChain.process(request.mainText());
            } catch (InvalidCPException invalidCPException) {
                // TODO:
                sender.sendError(request.messageId(), invalidCPException.getMessage());
                return;
            }
            String fileLink = pdfGenerator.generate(request.messageId(),
                                                    request.mainText());
            if (fileLink == null) {
                sender.sendError(request.messageId(),
                                 errorsMessages.fileError());
                return;
            }
            if (manager.saveCP(request.messageId(), fileLink)) {
                sender.sendCP(request.messageId(), fileLink);
//                sender.sendOk(request.messageId());
            } else {
                sender.sendError(request.messageId(), errorsMessages.dbError());
            }
        });

    }

}