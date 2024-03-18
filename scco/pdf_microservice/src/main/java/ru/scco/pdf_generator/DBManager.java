package ru.scco.pdf_generator;

import org.springframework.stereotype.Component;

@Component
public class DBManager {
    public boolean saveCP(long userId, String fileLink) {
        return true;
    }
}
