package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import ru.scco.pdf_generator.dto.DBInsertAllResponseDTO;
import ru.scco.pdf_generator.dto.DBInsertOneResponseDTO;
import ru.scco.pdf_generator.dto.PDFGeneratorRequestDTO;
import ru.scco.pdf_generator.processors.ProcessingChain;

import java.util.Base64;
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
        log.info("got request" + request);
        generatorPool.execute(() -> {
            String cp;
            try {
                log.info("start process");
                cp = new String(Base64.getDecoder().decode(request.mainText()));
                cp = processingChain.process(cp);
            } catch (InvalidCPException invalidCPException) {
                // TODO:
                log.info("invalid cp" + invalidCPException.getMessage());
                sender.sendError(request.messageId(), invalidCPException.getMessage());
                return;
            }
            log.info("start generating");
            String fileLink = pdfGenerator.generate(request.messageId(),
                                                    cp);
            log.info("end generating");
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
        log.info("got response:" + responses);
        for (DBInsertOneResponseDTO response :  responses.getResponses()) {
            sender.sendCPToOutput(response.getCustomerID(),
                                  response.getClientID(), response.getFilePath());
        }
    }

}