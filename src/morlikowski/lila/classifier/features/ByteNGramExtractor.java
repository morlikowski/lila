package morlikowski.lila.classifier.features;

import java.nio.charset.Charset;
import java.util.LinkedList;
import java.util.List;

public class ByteNGramExtractor implements FeatureExtractor {
	
	private final int N;
	
	public ByteNGramExtractor(int n) {
		this.N = n > 0 ? n : 1;
	}
	
	/**
	 * Extracts byte n-grams from the input string. The resulting n-grams have length n, not length 0 to n. No padding is used.  
	 * Note that the implementation is still encoding dependent, counteracting part of the reason to use byte n-grams
	 * in the first place.
	 * 
	 * @param 	text	a string assumed to hold some document text
	 * @return 			a list of strings which are literal representations of the decimal byte values (0-255).
	 * 
	 */
	@Override
	public List<String> extract(String text) {
		List<String> ngrams = new LinkedList<>();
		byte[] bytes = text.getBytes(Charset.forName("UTF-8"));
		for (int i = 0; i <= bytes.length - N; i++) {
			StringBuilder byteString = new StringBuilder();
			for (int j = i; j < i + N; j++) {
				String singleByteString = Byte.toString(bytes[j]);
				byteString.append(singleByteString);
			}
			ngrams.add(byteString.toString());
		}
		return ngrams;
	}

}
