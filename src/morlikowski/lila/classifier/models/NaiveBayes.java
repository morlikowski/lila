package morlikowski.lila.classifier.models;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.stream.Collectors;

import morlikowski.lila.classifier.features.FeatureExtractor;
import morlikowski.lila.corpus.Document;
import morlikowski.lila.util.Pair;

public class NaiveBayes implements Classifier {

	private Map<String, Map<String, Double>> probabilities = new HashMap<>();
	private Map<String, Double> probabilitiesOfUnknown = new HashMap<>();

	private final static int FIRST_ELEMENT = 0;
	
	private final FeatureExtractor feature;
	
	public NaiveBayes(FeatureExtractor feature) {
		this.feature = feature;
	}

	@Override
	public void train(List<Document> docs) {

		Map<String, Integer> totalsPerLanguage = new HashMap<>();

		/*
		 * This loop iterates through all training documents and
		 * 
		 * 1) extracts features
		 * 
		 * 2) calculates the number of times a specific word/n-gram w occurs with a specific language
		 * 	  and stores it in this.probabilities for further processing
		 * 
		 * 3) calculates the total number of words/n-grams that occur with a specific language
		 * 	  and stores it in totalsPerLanguage
		 */
		for (Document doc : docs) {
			String language;
			try {
				language = doc.getSingletonLabel();
			} catch (Exception e) {
				e.printStackTrace();
				continue;
			}
			List<String> ngrams = this.feature.extract(doc.getText());
			Map<String, Double> ngram_counts;
			Integer sum_per_language;

			if (probabilities.containsKey(language)) {
				ngram_counts = probabilities.get(language);
			} else {
				ngram_counts = new HashMap<>();
			}

			if (totalsPerLanguage.containsKey(language)) {
				sum_per_language = totalsPerLanguage.get(language);
			} else {
				sum_per_language = 0;
			}

			for (String ngram : ngrams) {
				if (ngram_counts.containsKey(ngram)) {
					Double current_count = ngram_counts.get(ngram);
					ngram_counts.put(ngram, current_count + 1d);
				} else {
					ngram_counts.put(ngram, 1d);
				}
			}

			totalsPerLanguage.put(language, sum_per_language + ngrams.size());
			probabilities.put(language, ngram_counts);

		}
		
		/*
		 * Calculates the size of the vocabulary (cardinality of the set of all words/n-grams in the training data) 
		 */
		Integer sizeOfVocabulary = NaiveBayes.calculateSizeOfVocabulary(this.probabilities);

		/*
		 *  Calculates the probability of an unknown word for each language using Laplace smoothing for count=0
		 */
		this.probabilitiesOfUnknown = NaiveBayes.calculateProbabilitiesOfUnknown(totalsPerLanguage, sizeOfVocabulary);

		/*
		 * Transforms the counts in this.probabilities to log-transformed and smoothed probabilities
		 */
		for (Entry<String, Map<String, Double>> countMapEntry : this.probabilities.entrySet()) {
			String language = countMapEntry.getKey();
			Integer n = totalsPerLanguage.get(language);
			countMapEntry.getValue().replaceAll((ngram, count) -> NaiveBayes
					.calculateSmoothedLogProbability(count.intValue(), n, sizeOfVocabulary));
		}

	}
	
	private static Integer calculateSizeOfVocabulary(Map<String, Map<String, Double>> probabilities) {
		return probabilities.values().stream()
		.flatMap(ngramProbabilites -> ngramProbabilites.keySet().stream())
		.collect(Collectors.toSet())
		.size();
	}
	
	private static Map<String, Double> calculateProbabilitiesOfUnknown (Map<String, Integer> totalsPerLanguage, Integer sizeOfVocabulary) {
		Map<String, Double> probabilitiesOfUnknown = new HashMap<>();
		for (Entry<String, Integer> sumOfNGrams : totalsPerLanguage.entrySet()) {
			String language = sumOfNGrams.getKey();
			Integer count = 0;
			Double probabilityOfUnknown = NaiveBayes.calculateSmoothedLogProbability(count, sumOfNGrams.getValue(),
					sizeOfVocabulary);
			probabilitiesOfUnknown.put(language, probabilityOfUnknown);
		}
		return probabilitiesOfUnknown;
	}

	private static Double calculateSmoothedLogProbability(Integer count, Integer n, Integer sizeOfVocabulary) {
		return Math.log((count + 1d) / (n + sizeOfVocabulary + 1d));
	}
	
	@Override
	public Set<String> predict(String text) {
		List<String> ngrams = this.feature.extract(text);
		List<Pair<String, Double>> predicted = new LinkedList<>();
		Set<String> finalPrediction = new HashSet<>();
		for (Entry<String, Map<String, Double>> probabilityEntry : this.probabilities.entrySet()) {
			String language = probabilityEntry.getKey();
			Map<String, Double> probabilityOfLanguage = probabilityEntry.getValue();
			Double probability = 0d;
			Double defaultProbability = this.probabilitiesOfUnknown.get(language);
			for (String ngram : ngrams) {
				probability += probabilityOfLanguage.getOrDefault(ngram, defaultProbability);
			}
			predicted.add(new Pair<String, Double>(language, probability));
		}
		predicted.sort((predictionA, predictionB) -> Double.compare(predictionB.second, predictionA.second));
		String predictedLabel = predicted.get(FIRST_ELEMENT).first;
		finalPrediction.add(predictedLabel);
		return finalPrediction;
	}

}
