package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.cos.COSDictionary;
import org.apache.pdfbox.multipdf.LayerUtility;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.PDPageTree;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDFont;
import org.apache.pdfbox.pdmodel.font.PDType0Font;
import org.apache.pdfbox.pdmodel.graphics.form.PDFormXObject;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotation;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotationWidget;
import org.apache.pdfbox.pdmodel.interactive.form.PDAcroForm;
import org.apache.pdfbox.pdmodel.interactive.form.PDTextField;

import java.awt.geom.AffineTransform;
import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Objects;

@Slf4j
@RequiredArgsConstructor
public class PDFGenerator {
    private final String templatePath;
    private final String fontPath;
    private final String destinationPath;
    private final int fontSize;


    private record Pair(String restText, float lineY) {
    }


    // Если указан размер и цвет шрифта поля - он применяется
    // Иначе по умолчанию - черный
    private int setAppearance(PDPageContentStream contentStream,
                                     String appearance, PDFont font)
            throws IOException {
        int fontSize = this.fontSize;
        if (appearance != null) {
            String[] styleSettings = appearance.split(" ");
            if (styleSettings.length == 7) {
                fontSize = Integer.parseInt(styleSettings[1]);
                contentStream.setNonStrokingColor(
                        Float.parseFloat(styleSettings[3]),
                        Float.parseFloat(styleSettings[4]),
                        Float.parseFloat(styleSettings[5]));
            }
        }
        contentStream.setFont(font, fontSize);
        return fontSize;
    }

    // Connection with page may not know about its page,
    // But page has to know about widgets
    // Method finds page that contains certain widget
    private static PDPage getPdPage(PDDocument document,
                                    PDAnnotationWidget widget)
            throws IOException {
        PDPage page = widget.getPage();
        if (page == null) {
            PDPageTree pages = document.getPages();
            for (int i = 0; i < pages.getCount(); ++i) {
                for (PDAnnotation annotation : pages.get(i).getAnnotations()) {
                    COSDictionary annotationObject = annotation.getCOSObject();
                    if (annotationObject.equals(widget.getCOSObject())) {
                        page = pages.get(i);
                        i = pages.getCount();
                        break;
                    }
                }
            }
        }
        return page;
    }


    // метод переноса строки в длинном тексте
    // пытается переносить по пробелу
    // Проблема pdf, что разные символы имеют разный размер, поэтому приходится
    // на каждом пробеле проверять, нужен ли перенос
    // TODO: указывать приблизительную позицию через averageFontSize, потом
    // добирать / убирать символы.
    private static Pair showLongLine(String text,
                                     PDPageContentStream contentStream,
                                     PDFont font, int fontSize,
                                     PDRectangle rectangle, float y)
            throws IOException {
        float maxCharWidth = fontSize * font.getWidth('ж') / 1000;
        float deltaY = -fontSize * (font.getBoundingBox()
                                        .getHeight()) / 1000;
        y += deltaY;
        contentStream.newLineAtOffset(0, deltaY);
        int lastSpace = -1;
        while (!text.isEmpty()) {
            if (y < rectangle.getLowerLeftY()) {
                return new Pair(text, y);
            }
            int spaceIndex = text.indexOf(' ', lastSpace + 1);
            if (spaceIndex < 0) {
                spaceIndex = text.length();
            }
            String subString = text.substring(0, spaceIndex);
            float size = fontSize * font.getStringWidth(subString) / 1000;
            if (size > rectangle.getUpperRightX() - rectangle.getLowerLeftX()) {
                if (lastSpace < 0) {
                    System.out.println(maxCharWidth);
                    lastSpace = (int) (rectangle.getWidth() / maxCharWidth);
                }
                contentStream.showText(subString.substring(0, lastSpace));
                contentStream.newLineAtOffset(0, deltaY);
                y += deltaY;
                text = text.substring(lastSpace).trim();
                lastSpace = -1;
            } else if (spaceIndex == text.length()) {
                contentStream.showText(text);
                contentStream.newLineAtOffset(0, deltaY);
                y += deltaY;
                text = "";
            } else {
                lastSpace = spaceIndex;
            }
        }
        return new Pair("", y);
    }

    private String fillMultiPageTemplate(long messageID,
                                         String mainText) {
        try (PDDocument doc = Loader.loadPDF(new File(Objects.requireNonNull(
                                                                     PDFGenerator.class.getResource(templatePath))
                                                             .toURI()))) {
            PDFont font = PDType0Font.load(doc,
                                           PDFGenerator.class.getResourceAsStream(
                                                   fontPath), false);

            PDAcroForm acroForm = doc.getDocumentCatalog().getAcroForm();
            PDTextField template = (PDTextField) acroForm.getField("main_text");

            PDRectangle rectangle = template.getWidgets().get(0).getRectangle();
            PDPage page = doc.getPage(0);
            LayerUtility layerUtility = new LayerUtility(doc);
            PDFormXObject firstForm =
                    layerUtility.importPageAsForm(doc, 0);
            AffineTransform affineTransform = new AffineTransform();

            PDPageContentStream contentStream =
                    new PDPageContentStream(doc, page,
                                            PDPageContentStream.AppendMode.APPEND,
                                            false, true);
            int fontSize = setAppearance(contentStream,
                                         template.getDefaultAppearance(), font);
            contentStream.beginText();
            contentStream.setFont(font, fontSize);

            contentStream.newLineAtOffset(rectangle.getLowerLeftX(),
                                          rectangle.getUpperRightY());
            float y = rectangle.getUpperRightY();
            int cnt = 0;
            Deque<String> lines =
                    new ArrayDeque<>(Arrays.asList(mainText.split("\n")));
            while (!lines.isEmpty()) {
                Pair positionAndRest =
                        showLongLine(lines.removeFirst(), contentStream, font,
                                     fontSize,
                                     rectangle,
                                     y);
                y = positionAndRest.lineY();
                if (y < rectangle.getLowerLeftY()) {
                    contentStream.endText();
                    contentStream.close();
                    page = new PDPage(page.getMediaBox());
                    doc.addPage(page);
                    layerUtility.appendFormAsLayer(page, firstForm,
                                                   affineTransform,
                                                   "page" + cnt);
                    cnt++;
                    contentStream = new PDPageContentStream(doc, page,
                                                            PDPageContentStream.AppendMode.APPEND,
                                                            false, true);
                    contentStream.beginText();
                    contentStream.setFont(font, fontSize);

                    contentStream.newLineAtOffset(rectangle.getLowerLeftX(),
                                                  rectangle.getUpperRightY());
                    y = rectangle.getUpperRightY();
                    lines.addFirst(positionAndRest.restText);
                }
            }

            contentStream.endText();
            contentStream.close();

            acroForm.flatten();
            Path filePath = Path.of(destinationPath, messageID + ".pdf");
            doc.save(filePath.toAbsolutePath().toString());
            return filePath.toString();
        } catch (IOException | URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }

    public String generate(long messageId, String cp) {
        return fillMultiPageTemplate(messageId, cp);
    }
}