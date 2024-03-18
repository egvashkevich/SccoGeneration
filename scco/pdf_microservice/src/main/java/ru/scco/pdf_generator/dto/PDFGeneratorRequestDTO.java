package ru.scco.pdf_generator.dto;

import java.io.Serializable;

public record PDFGeneratorRequestDTO(long senderId, String cp) implements
                                                               Serializable {
}
