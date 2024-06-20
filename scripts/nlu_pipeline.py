import nltk
import spacy
from transformers import pipeline

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Hugging Face pipeline for intent classification
intent_classifier = pipeline("zero-shot-classification")

def tokenize(text):
    """
    Tokenize the input text using NLTK.
    """
    tokens = nltk.word_tokenize(text)
    return tokens

def named_entity_recognition(text):
    """
    Perform Named Entity Recognition (NER) using spaCy.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def classify_intent(text, candidate_labels):
    """
    Classify the intent of the input text using Hugging Face zero-shot classification.
    """
    result = intent_classifier(text, candidate_labels)
    return result

def main():
    # Example usage
    text = "Book a flight to New York for tomorrow."
    candidate_labels = ["travel", "booking", "weather", "news"]

    tokens = tokenize(text)
    entities = named_entity_recognition(text)
    intent = classify_intent(text, candidate_labels)

    print("Tokens:", tokens)
    print("Entities:", entities)
    print("Intent:", intent)

if __name__ == "__main__":
    main()
