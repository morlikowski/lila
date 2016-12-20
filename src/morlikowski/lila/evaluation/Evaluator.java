package morlikowski.lila.evaluation;

import java.util.List;
import java.util.Set;

import morlikowski.lila.classifier.models.Classifier;
import morlikowski.lila.corpus.Document;

public class Evaluator {
	
	public static void test (List<Document> docs, Classifier model) {
		
		Float rightPredictions = 0f;
		Float n = new Float(docs.size());
		
		for (Document doc : docs) {
			Set<String> predictedLabels = model.predict(doc.getText());
			if(predictedLabels.containsAll((doc.getLabels()))) {
				rightPredictions += 1;
			}
		}
		
		System.out.println("Accuracy: " + rightPredictions / n);
	}
}
