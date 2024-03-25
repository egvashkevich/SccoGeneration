package ru.scco.pdf_generator;

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
import java.util.Objects;

//@Component
@Slf4j
public class PDFGenerator {
    private final String templatePath;
    private final String fontPath;
    private final String destinationPath;

    public PDFGenerator(String templatePath,
                        String fontPath, String destinationPath) {
        this.templatePath = templatePath;
        this.fontPath = fontPath;
        this.destinationPath = destinationPath;
    }


    private static void handleTemplate(PDTextField template,
                                       PDAcroForm acroForm,
                                       PDPage page,
                                       String fontName,
                                       String value) throws IOException {
        PDTextField mainTextBox = new PDTextField(acroForm);
        mainTextBox.setPartialName(template.getPartialName() + "_generated");
        mainTextBox.setMultiline(template.isMultiline());
        mainTextBox.setDefaultAppearance(template.getDefaultAppearance()
                                                 .replaceAll("/\\w+",
                                                             "/" + fontName));
        mainTextBox.getWidgets().get(0).setRectangle(
                template.getWidgets().get(0).getRectangle());
        mainTextBox.getWidgets().get(0).setPage(page);
        page.getAnnotations().add(mainTextBox.getWidgets().get(0));
        template.setReadOnly(true);
        mainTextBox.setReadOnly(true);
        acroForm.getFields().add(mainTextBox);
        mainTextBox.setValue(value);
        template.setValue(null);

    }

    public String generate(long senderId, String cp, String signature)
            throws IOException {
        try (PDDocument doc = Loader.loadPDF(
                new File(Objects.requireNonNull(
                                        PDFGenerator.class.getResource(templatePath))
                                .toURI()))) {
            PDPage page = doc.getPage(0);
            PDAcroForm acroForm = doc.getDocumentCatalog().getAcroForm();
            PDFont formFont = PDType0Font.load(
                    doc,
                    PDFGenerator.class.getResourceAsStream(fontPath),
                    false);
            PDResources resources = acroForm.getDefaultResources();
            final String fontName = resources.add(formFont).getName();
            handleTemplate((PDTextField) acroForm
                                   .getField("main_text"),
                           acroForm,
                           page,
                           fontName,
                           cp
            );
            handleTemplate((PDTextField) acroForm
                                   .getField("signature"),
                           acroForm,
                           page,
                           fontName,
                           signature
            );
            String fileName = destinationPath + senderId +
                              ".pdf";
            doc.save(fileName);
            return fileName;
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }
}