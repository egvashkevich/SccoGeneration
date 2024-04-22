package ru.scco.pdf_generator.processors;

import org.springframework.stereotype.Component;
import ru.scco.pdf_generator.InvalidCPException;

import java.util.ArrayList;
import java.util.List;

@Component
public class ProcessingChain implements ProcessNode {

    List<ProcessNode> processNodeList = new ArrayList<>();

    public ProcessingChain() {
        processNodeList.add(new DeleteInPart(0.7f, 1,
                                             "(?:^|[.!?;])[^.!?;]*уважени[^"
                                             + ".!?;$\\n]*(?:[.!?;\\n]|$)"));
    }

    ProcessingChain append(ProcessNode processNode) {
        processNodeList.add(processNode);
        return this;
    }

    public String process(String cp) throws InvalidCPException {
        for (ProcessNode node : processNodeList) {
            String newCP = node.process(cp);
            if (newCP != null) {
                cp = newCP;
            }
        }
        if (cp.length() < 100) {
            throw new InvalidCPException("too small CP");
        }
        return cp;
    }
}
