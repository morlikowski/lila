package morlikowski.lila;

import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import morlikowski.lila.classifier.features.ByteNGramExtractor;
import morlikowski.lila.classifier.features.CharNGramExtractor;
import morlikowski.lila.classifier.features.FeatureExtractor;
import morlikowski.lila.classifier.models.Classifier;
import morlikowski.lila.classifier.models.NaiveBayes;
import morlikowski.lila.corpus.ALTW2010Corpus;
import morlikowski.lila.corpus.Corpus;
import morlikowski.lila.corpus.Document;
import morlikowski.lila.corpus.LIGACorpus;
import morlikowski.lila.evaluation.Evaluator;

public class Main {

	public static void main(String[] args) {
		Corpus train = new LIGACorpus();
		train.load("data/liga/liga_learn");
		FeatureExtractor charNGrams = new CharNGramExtractor(3);
		Classifier model = new NaiveBayes(charNGrams);
		model.train(train.getDocuments());
		Corpus test = new LIGACorpus();
		test.load("data/liga/liga_test");
		Evaluator.test(test.getDocuments(), model);
		
		String englishText = "The Knight's Cross of the Iron Cross and its higher grades were based on four separate enactments. The first enactment, Reichsgesetzblatt I S. 1573 of 1 September 1939 instituted the Iron Cross (Eisernes Kreuz), the Knight's Cross of the Iron Cross and the Grand Cross of the Iron Cross (Großkreuz des Eisernen Kreuzes). Article 2 of the enactment mandated that the award of a higher class be preceded by the award of all preceding classes.";
		String germanText = "Das Trägheitsmoment, auch Massenträgheitsmoment oder Inertialmoment, gibt den Widerstand eines starren Körpers gegenüber einer Änderung seiner Rotationsbewegung um eine gegebene Achse an (Drehmoment geteilt durch Winkelbeschleunigung). Damit spielt es die gleiche Rolle wie im Verhältnis von Kraft und Beschleunigung die Masse; deswegen ist in der älteren Literatur auch die Bezeichnung Drehmasse gebräuchlich. Als physikalische Größe kommt es erstmals 1740 im Werk Theoria motus corporum solidorum seu rigidorum von Leonhard Euler vor. Das Trägheitsmoment hängt von der Massenverteilung in Bezug auf die Drehachse ab. Je weiter ein Massenelement von der Drehachse entfernt ist, desto mehr trägt es zum Trägheitsmoment bei; der Abstand geht quadratisch ein. Nimmt";
		
		System.out.println("Anecdotal evidence using two Wikipedia fragments:");
		System.out.println(englishText);
		System.out.println("Predicted: " + model.predict("The Knight's Cross of the Iron Cross and its higher grades were based on four separate enactments. The first enactment, Reichsgesetzblatt I S. 1573 of 1 September 1939 instituted the Iron Cross (Eisernes Kreuz), the Knight's Cross of the Iron Cross and the Grand Cross of the Iron Cross (Großkreuz des Eisernen Kreuzes). Article 2 of the enactment mandated that the award of a higher class be preceded by the award of all preceding classes."));
		System.out.println(germanText);
		System.out.println("Predicted: " + model.predict("Das Trägheitsmoment, auch Massenträgheitsmoment oder Inertialmoment, gibt den Widerstand eines starren Körpers gegenüber einer Änderung seiner Rotationsbewegung um eine gegebene Achse an (Drehmoment geteilt durch Winkelbeschleunigung). Damit spielt es die gleiche Rolle wie im Verhältnis von Kraft und Beschleunigung die Masse; deswegen ist in der älteren Literatur auch die Bezeichnung Drehmasse gebräuchlich. Als physikalische Größe kommt es erstmals 1740 im Werk Theoria motus corporum solidorum seu rigidorum von Leonhard Euler vor. Das Trägheitsmoment hängt von der Massenverteilung in Bezug auf die Drehachse ab. Je weiter ein Massenelement von der Drehachse entfernt ist, desto mehr trägt es zum Trägheitsmoment bei; der Abstand geht quadratisch ein. Nimmt"));
	}
	
	/*
	 * Corpus altw = new ALTW2010Corpus();
		altw.load(Paths.get("data/altw2010/trn"));
		altw.getDocuments().stream().forEach(System.out::println);
	 */

}
