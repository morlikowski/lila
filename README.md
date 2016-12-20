# What is Lila?
Lila is an experimental collection of corpora and models (written in Java) for language identification, i.e. determining the (natural) language of a given document.


# How do I use it?

For example, training and evaluating a Naive Bayes classifier (with character-trigrams as features) on the LIGA corpus
looks like this:

```java
Corpus train = new LIGACorpus();
train.load("data/liga/liga_learn");
FeatureExtractor charNGrams = new CharNGramExtractor(3);
Classifier model = new NaiveBayes(charNGrams);
model.train(train.getDocuments());
Corpus test = new LIGACorpus();
test.load("data/liga/liga_test");
Evaluator.test(test.getDocuments(), model);
```
Concrete models, corpora and feature extractors are described within a minimal set of interfaces and abstract classes. These describe the workflow of training a classifier (with a certain feature extractor) on a corpus and then evaluating the resulting model on test data:

```java
Corpus train = new ClassWhichImplementsCorpus();
train.load(Paths.get("path/to/train"));
FeatureExtractor extractor = new ClassWhichImplementsFeatureExtractor();
Classifier model = new ClassWhichImplemenmentsClassifier(extractor);
model.train(train.getDocuments());
Corpus test = new ClassWhichImplementsCorpus();
test.load(Paths.get("path/to/test"));
Evaluator.test(test.getDocuments(), model);
```

# What is missing?
- multilingual language identification
- more detailed evaluation (precision, recall, F1, cross-validation)
- more flexible feature extraction
- feature selection
- more models (e.g. Mixture Models, cf. Lui et al. 2014)

# Models

## NaiveBayes

Multinomial Naive Bayes model (cf. McCallum & Nigam 1998) with Laplace (add-one) smoothing.


## MixtureModel (TODO)

An implementation of the generative mixture model (cf. Griffiths & Steyvers 2004) presented by Lui et al. 2014.

# References

## Monolingual
http://www.aclweb.org/anthology/W/W14/W14-5316.pdf
http://www.aclweb.org/anthology/P12-3005
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.9324
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.9367
http://www.win.tue.nl/~mpechen/publications/pubs/TrompPechenizkiy_LIGA_Benelearn11.pdf
"Language Identification from Text Using N-gram Based Cumulative Frequency Addition"

## Multilingual
http://www.aclweb.org/anthology/Q14-1003
http://www.aclweb.org/anthology/I11-1062
http://www.alta.asn.au/events/alta2010/proceedings/pdf/U10-1003.pdf

## Datasets

### Multilingual Wikipedia
http://people.eng.unimelb.edu.au/tbaldwin/etc/wikipedia-multi-v5.tgz

### ALTW 2010
http://people.eng.unimelb.edu.au/tbaldwin/etc/altw2010-langid.tgz

### LIGA
https://github.com/llaisdy/liga 


## Naive Bayes
http://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf

## Mixture Models
Thomas L. Griffiths and Mark Steyvers. 2004. Finding scientific topics.
http://psiexp.ss.uci.edu/research/papers/sciencetopics.pdf
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.35.888
