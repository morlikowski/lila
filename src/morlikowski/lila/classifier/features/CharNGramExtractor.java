package morlikowski.lila.classifier.features;

import java.util.LinkedList;
import java.util.List;

public class CharNGramExtractor implements FeatureExtractor {

	private final int N;

	public CharNGramExtractor(int n) {
		this.N = n > 0 ? n : 1;
	}

	@Override
	public List<String> extract(String docText) {
		List<String> ngrams = new LinkedList<>();
		String text = CharNGramExtractor.addPadding(docText, N - 1);
		for (int i = 0; i <= text.length() - N; i++) {
			ngrams.add(text.substring(i, i + N));
		}
		return ngrams;
	}
	
	private static String addPadding(String text, int size) {
		if (size > 0) {
			StringBuilder builder = new StringBuilder();
			for (int i = 0; i < size; i++) {
				builder.append("_");
			}
			String padding = builder.toString();
			return "_" + text + padding;
		} else {
			return text;
		}
	}

}
