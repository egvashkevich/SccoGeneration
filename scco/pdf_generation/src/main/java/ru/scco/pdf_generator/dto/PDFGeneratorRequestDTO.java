package ru.scco.pdf_generator.dto;

import java.io.Serializable;

public record PDFGeneratorRequestDTO(long queryId, long senderId, String cp,
                                     String signature) implements
                                                       Serializable {
}
