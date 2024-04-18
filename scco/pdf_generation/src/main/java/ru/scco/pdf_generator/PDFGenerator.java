package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.io.IOUtils;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDResources;
import org.apache.pdfbox.pdmodel.font.PDFont;
import org.apache.pdfbox.pdmodel.font.PDType0Font;
import org.apache.pdfbox.pdmodel.interactive.form.PDAcroForm;
import org.apache.pdfbox.pdmodel.interactive.form.PDTextField;

import java.io.IOException;
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
        try (PDDocument doc = Loader.loadPDF(IOUtils.toByteArray(
                Objects.requireNonNull(
                        PDFGenerator.class.getResourceAsStream(
                                templatePath))))) {
            PDPage page = doc.getPage(0);
            PDAcroForm acroForm = doc.getDocumentCatalog().getAcroForm();

            PDFont formFont = PDType0Font.load(doc,
                                               PDFGenerator.class.getResourceAsStream(
                                                       fontPath), false);
            PDResources resources = acroForm.getDefaultResources();
            String fontName = resources.add(formFont).getName();
            handleTemplate((PDTextField) acroForm.getField("main_text"),
                           acroForm, page, fontName, cp);
            handleTemplate((PDTextField) acroForm.getField("signature"),
                           acroForm, page, fontName, signature);
            Path directory = Path.of(destinationPath, String.valueOf(senderId));
            Files.createDirectories(directory);
            acroForm.flatten();
            Path filePath = Path.of(directory.toString(), queryId + ".pdf");
            doc.save(filePath.toAbsolutePath().toString());
            return filePath.toString();
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