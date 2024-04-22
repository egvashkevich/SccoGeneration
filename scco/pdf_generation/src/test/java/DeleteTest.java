import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import ru.scco.pdf_generator.InvalidCPException;
import ru.scco.pdf_generator.processors.ProcessingChain;


public class DeleteTest {
    ProcessingChain chain = new ProcessingChain();

    @Test
    public void nothingToDeleteTest() throws InvalidCPException {
        String cp = "Все говорят: Кремль, Кремль. Ото всех я слышал про него,"
                    + " а сам ни разу не видел. Сколько раз уже (тысячу раз),"
                    + " напившись, или с похмелюги, проходил по Москве с севера на юг, с запада на восток, из конца в конец и как попало — и ни разу не видел Кремля.";
        Assertions.assertEquals(cp, chain.process(cp));
    }

    @Test
    public void oneSentenceToDelete() throws InvalidCPException {
        String cp = "- И немедленно выпил… - Нет, вот уж теперь — жить и "
                    + "жить! А жить совсем не скучно! Скучно было жить только"
                    + " Николаю Гоголю и царю Соломону. Если уж мы прожили тридцать лет, надо попробовать прожить еще тридцать, да, да. «Человек смертен» — таково мое мнение. Но уж если мы родились, ничего не поделаешь — надо немножко пожить… «Жизнь прекрасна» — таково мое мнение.";
        String partToDelete = "С уважением, Панки";
        Assertions.assertEquals(cp, chain.process(cp + partToDelete));
    }

    @Test
    public void twoSentenceToDelete() throws InvalidCPException {
        String cp = "- И немедленно выпил… - И немедленно выпил… - Нет, вот уж теперь — жить и "
                    + "жить! А жить совсем не скучно! Скучно было жить только"
                    + " Николаю Гоголю и царю Соломону. Если уж мы прожили тридцать лет, надо попробовать прожить еще тридцать, да, да. «Человек смертен» — таково мое мнение. Но уж если мы родились, ничего не поделаешь — надо немножко пожить… «Жизнь прекрасна» — таково мое мнение.";
        String partToDelete = "С уважением, Панки.";
        System.out.println(chain.process(cp + partToDelete + partToDelete));
        Assertions.assertEquals(cp, chain.process(cp + partToDelete + partToDelete));
    }

    @Test
    public void tooSmallCPTest() throws InvalidCPException {
        Assertions.assertThrows(InvalidCPException.class, ()->chain.process(
                "- И немедленно выпил…"));
    }
}
