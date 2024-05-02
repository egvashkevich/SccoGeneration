package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

public class PDFCpResponseDTO implements
                              Serializable {
    @JsonProperty("message_group_id")
    long userId;
    @JsonProperty("file_path")
    String CPlink;

    public PDFCpResponseDTO(long userId, String CPlink) {
        this.userId = userId;
        this.CPlink = CPlink;
    }
}
