import spacy
from nltk.corpus import stopwords
nlp = spacy.load("pt_core_news_sm")
import regex as re
from unidecode import unidecode
from spacy.lang.pt.stop_words import STOP_WORDS
from nltk.corpus import stopwords
from nltk import word_tokenize

def preprocess(relato):
    def remove_stop_words(relato):
        # Remove stop words em português
        sw = list(set(stopwords.words('portuguese') + list(STOP_WORDS)))
        sw = [unidecode(word).lower() for word in sw]
        return ' '.join([token for token in word_tokenize(relato) if len(token) > 2 and token not in sw])
    
    def clean_relato(relato):
        # Remoção de números e pontuação
        relato = re.sub(r'(<[^<>]*>)|(&nvsp;)', " ", relato)
        relato = re.sub(r"[^\w\s]", " ", relato)
        relato = re.sub(r"[\d]", " ", relato)
        relato = remove_stop_words(relato)
        return relato
    
    def extract_lemmas(relato):
        # Extração do lemma
        return [str(word.lemma_).lower() for word in nlp(relato)]
    
    relato = clean_relato(relato)
    relato = extract_lemmas(relato)
    return relato