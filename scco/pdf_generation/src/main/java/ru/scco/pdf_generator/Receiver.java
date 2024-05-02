package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import ru.scco.pdf_generator.dto.DBInsertAllResponseDTO;
import ru.scco.pdf_generator.dto.DBInsertOneResponseDTO;
import ru.scco.pdf_generator.dto.PDFGeneratorRequestDTO;
import ru.scco.pdf_generator.processors.ProcessingChain;

import java.util.concurrent.ExecutorService;

@Slf4j
@Service
@RequiredArgsConstructor
public class Receiver {
    private final PDFGenerator pdfGenerator;
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
                                                    cp);
            if (fileLink == null) {
                sender.sendError(request.messageId(),
                                 errorsMessages.fileError());
                return;
            }
            sender.sendCPToDB(request.messageId(), fileLink);
        });

    }


    @RabbitListener(queues = {"${rabbit.db_response_queue}"})
    public void consumeDBResponse(DBInsertAllResponseDTO responses) {
        for (DBInsertOneResponseDTO response :  responses.getResponses()) {
            sender.sendCPToOutput(response.getCustomerID(),
                                  response.getClientID(), response.getFilePath());
        }
    }

}