package morlikowski.lila.classifier.features;

import java.util.List;

public interface FeatureExtractor {
	
	public List<String> extract(String text);
	
}
