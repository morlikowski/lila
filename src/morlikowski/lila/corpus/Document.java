package morlikowski.lila.corpus;

import java.util.HashSet;
import java.util.Set;

public class Document {
	
	private Set<String> labels;
	private String text;
	
	public Document(String label, String text) {
		Set<String> labelsSet = new HashSet<>();
		labelsSet.add(label);
		this.setLabels(labelsSet);
		this.setText(text);
	}
	
	public Document(Set<String> labels, String text) {
		this.setLabels(labels);
		this.setText(text);
	}

	public Set<String> getLabels() {
		return labels;
	}
	
	public String getSingletonLabel() throws Exception {
		if (this.labels.size() == 1) {
			return this.labels.iterator().next();
		} else {
			throw new Exception();
		}
	}

	public void setLabels(Set<String> labels) {
		this.labels = labels;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}
	
	public String toString() {
		String printText = "";
		if(text.length() > 100) {
			printText = this.labels + ": " + this.text.substring(0, 99) + " (...)";
		} else {
			printText = this.labels + ": " + this.text;
		}
		return printText;
	}

}
