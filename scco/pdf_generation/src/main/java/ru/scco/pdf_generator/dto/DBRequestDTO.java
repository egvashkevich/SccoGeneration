package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class DBRequestDTO implements
                              Serializable {
    @JsonProperty("request_name")
    final String requestName = "insert_offers";

    @JsonProperty("request_data")
    List<PDFCpResponseDTO> responseDTOs = new ArrayList<>();

    @JsonProperty("reply")
    DBReplyDTO dbReplyDTO;

    public DBRequestDTO(PDFCpResponseDTO responseDTO, DBReplyDTO replyDTO) {
        this.responseDTOs.add(responseDTO);
        this.dbReplyDTO = replyDTO;
    }
}