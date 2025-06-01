# data_layer.py
import spacy

nlp = spacy.load("en_core_web_sm")

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def preprocess_text(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]
