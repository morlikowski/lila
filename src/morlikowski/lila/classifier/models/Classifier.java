package morlikowski.lila.classifier.models;

import java.util.List;
import java.util.Set;

import morlikowski.lila.corpus.Document;

public interface Classifier {
	
	public Set<String> predict(String docText);
	
	public void train(List<Document> docs);
	
}