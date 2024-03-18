package ru.scco.pdf_generator.dto;

import java.io.Serializable;

public record PDFCpResponseDTO(long userId, String CPlink) implements
                                                           Serializable {
}
