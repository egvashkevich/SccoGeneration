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
                cp = processingChain.process(request.cp());
            } catch (InvalidCPException invalidCPException) {
                sender.sendError(request.senderId(), invalidCPException.getMessage());
                return;
            }
            String fileLink = pdfGenerator.generate(request.queryId(),
                                                    request.senderId(),
                                                    cp,
                                                    request.signature());
            if (fileLink == null) {
                sender.sendError(request.senderId(),
                                 errorsMessages.fileError());
                return;
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