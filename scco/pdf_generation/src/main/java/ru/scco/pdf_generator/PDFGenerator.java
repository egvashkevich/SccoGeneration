package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDResources;
import org.apache.pdfbox.pdmodel.font.PDFont;
import org.apache.pdfbox.pdmodel.font.PDType0Font;
import org.apache.pdfbox.pdmodel.interactive.form.PDAcroForm;
import org.apache.pdfbox.pdmodel.interactive.form.PDTextField;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Objects;

@Slf4j
@RequiredArgsConstructor
public class PDFGenerator {
    private final String templatePath;
    private final String fontPath;
    private final String destinationPath;
    private final int fontSize;


    private static void handleTemplate(PDTextField template,
                                       PDAcroForm acroForm, PDPage page,
                                       String fontName, String value)
            throws IOException {
        PDTextField implementation = new PDTextField(acroForm);
        implementation.setPartialName(template.getPartialName() + "_generated");
        implementation.setMultiline(template.isMultiline());
        implementation.setDefaultAppearance(template.getDefaultAppearance()
                                                    .replaceAll("/\\w+", "/"
                                                                         + fontName));
        implementation.getWidgets().get(0).setRectangle(
                template.getWidgets().get(0).getRectangle());
        implementation.getWidgets().get(0).setPage(page);
        implementation.setValue(value);
        page.getAnnotations().add(implementation.getWidgets().get(0));
        acroForm.getFields().add(implementation);

        template.setReadOnly(true);
        template.setValue(null);
        template.getWidgets().get(0).setNoView(true);
        page.getAnnotations().remove(template.getWidgets().get(0));
        acroForm.getFields().remove(template);

    }

    public String generate(long queryId, long senderId, String cp,
                           String signature) {
        try (PDDocument doc = Loader.loadPDF(new File(Objects.requireNonNull(
                PDFGenerator.class.getResource(templatePath)).toURI()))) {
            PDPage page = doc.getPage(0);
            PDAcroForm acroForm = doc.getDocumentCatalog().getAcroForm();

            PDFont formFont = PDType0Font.load(doc,
                                               PDFGenerator.class.getResourceAsStream(
                                                       fontPath), false);
            PDResources resources = acroForm.getDefaultResources();
            final String fontName = resources.add(formFont).getName();

            handleTemplate((PDTextField) acroForm.getField("main_text"),
                           acroForm, page, fontName, cp);
            handleTemplate((PDTextField) acroForm.getField("signature"),
                           acroForm, page, fontName, signature);
            Path directory = Path.of(destinationPath, String.valueOf(senderId));
            Files.createDirectories(directory);
            acroForm.flatten();
            Path filePath = Path.of(directory.toString(), queryId + ".pdf");
            doc.save(filePath.toAbsolutePath().toString());
            System.out.println(filePath.toString());
            return filePath.toString();
        } catch (URISyntaxException e) {
            // Может возникнуть, только если мы накосячим с ресурсами
            log.error(e.getMessage());
            return null;
        } catch (IOException e) {
            // Так как чтение шаблона и шрифта без записи,
            // а запись производится в разные файлы, скорее всего
            // ошибка возникнет лишь при заполнении памяти. Нет смысла
            // повторять операцию
            log.error(e.getMessage());
            return null;
        }
    }
}


//package ru.scco.pdf_generator;
//
//import lombok.RequiredArgsConstructor;
//import lombok.extern.slf4j.Slf4j;
//import org.apache.pdfbox.Loader;
//import org.apache.pdfbox.pdmodel.PDDocument;
//import org.apache.pdfbox.pdmodel.PDPage;
//import org.apache.pdfbox.pdmodel.PDPageContentStream;
//import org.apache.pdfbox.pdmodel.PDResources;
//import org.apache.pdfbox.pdmodel.common.PDRectangle;
//import org.apache.pdfbox.pdmodel.font.PDFont;
//import org.apache.pdfbox.pdmodel.font.PDType0Font;
//import org.apache.pdfbox.pdmodel.interactive.form.PDAcroForm;
//import org.apache.pdfbox.pdmodel.interactive.form.PDTextField;
//
//import java.io.File;
//import java.io.IOException;
//import java.net.URISyntaxException;
//import java.util.Objects;
//
//@Slf4j
//@RequiredArgsConstructor
//public class PDFGenerator {
//    private final String templatePath;
//    private final String fontPath;
//    private final String destinationPath;
//    private final int fontSize;
//
//    // Добавляем переносы в длинной строке
//    // просто по количеству символов понять когда будет перенос нельзя
//    // так как разные символы в разных шрифтах имеют разный размер.
//    // Поэтому приходится на каждом пробеле проверять может ли предыдущая строка
//    // поместиться.
//    // Можно потом добавить предположение о размере, для русского текста сойдет
//
//    private static void showLongLine(String text,
//                                     PDPageContentStream contentStream,
//                                     PDFont font, int fontSize,
//                                     PDRectangle rectangle)
//            throws IOException {
//
//        float deltaY = -fontSize * (font.getBoundingBox()
//                                        .getHeight()) / 1000;
//        contentStream.newLineAtOffset(0, deltaY);
//        int lastSpace = -1;
//        while (!text.isEmpty()) {
//            int spaceIndex = text.indexOf(' ', lastSpace + 1);
//            if (spaceIndex < 0) {
//                spaceIndex = text.length();
//            }
//            String subString = text.substring(0, spaceIndex);
//            float size = fontSize * font.getStringWidth(subString) / 1000;
//            if (size > rectangle.getUpperRightX() - rectangle.getLowerLeftX()) {
//                if (lastSpace < 0) {
//                    lastSpace = spaceIndex;
//                }
//                contentStream.showText(subString.substring(0, lastSpace));
//                contentStream.newLineAtOffset(0, deltaY);
//                text = text.substring(lastSpace).trim();
//                lastSpace = -1;
//            } else if (spaceIndex == text.length()) {
//                contentStream.showText(text);
//                contentStream.newLineAtOffset(0, deltaY);
//                text = "";
//            } else {
//                lastSpace = spaceIndex;
//            }
//        }
//    }
//
//
//    private void handleTemplate(PDTextField template,
//                                PDDocument document,
//                                PDFont font,
//                                int fontSize,
//                                PDPage page,
//                                String value) throws IOException {
//        PDPageContentStream
//                contentStream = new PDPageContentStream(document, page,
//                                                        PDPageContentStream.AppendMode.APPEND,
//                                                        false, false);
//
//        contentStream.beginText();
//        contentStream.setFont(font, fontSize);
//        PDRectangle rectangle = template.getWidgets().get(0).getRectangle();
//        contentStream.newLineAtOffset(rectangle.getLowerLeftX(),
//                                      rectangle.getUpperRightY());
//        for (String line : value.split("\n")) {
//            showLongLine(line, contentStream, font,
//                         fontSize, template.getWidgets().get(0).getRectangle());
//        }
//        contentStream.endText();
//        contentStream.close();
//        template.setReadOnly(true);
//    }
//
//    public String generate(long senderId, String cp, String signature) {
//        try (PDDocument doc = Loader.loadPDF(
//                new File(Objects.requireNonNull(
//                                        PDFGenerator.class.getResource(templatePath))
//                                .toURI()))) {
//            PDPage page = doc.getPage(0);
//            PDAcroForm acroForm = doc.getDocumentCatalog().getAcroForm();
//            PDFont formFont = PDType0Font.load(
//                    doc,
//                    PDFGenerator.class.getResourceAsStream(fontPath),
//                    false);
//            handleTemplate((PDTextField) acroForm
//                                   .getField("main_text"),
//                           doc,
//                           formFont,
//                           fontSize,
//                           page,
//                           cp
//            );
//            handleTemplate((PDTextField) acroForm
//                                   .getField("signature"),
//                           doc,
//                           formFont,
//                           fontSize,
//                           page,
//                           signature
//            );
//            String fileName = destinationPath + senderId +
//                              ".pdf";
//            doc.save(fileName);
//            return fileName;
//        } catch (URISyntaxException e) {
//            // Может возникнуть, только если мы накосячим с ресурсами
//            log.error(e.getMessage());
//            return null;
//        } catch (IOException e) {
//            // Так как чтение шаблона и шрифта без записи,
//            // а запись производится в разные файлы, скорее всего
//            // ошибка возникнет лишь при заполнении памяти. Нет смысла
//            // повторять операцию
//            log.error(e.getMessage());
//            return null;
//        }
//    }
//}