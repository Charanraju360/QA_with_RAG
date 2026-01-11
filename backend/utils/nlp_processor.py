import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# download once
nltk.download("punkt")
nltk.download("stopwords")

def clean_text(text):
    tokens = word_tokenize(text.lower())
    stops = set(stopwords.words("english"))
    
    cleaned = [t for t in tokens if t.isalnum() and t not in stops]
    
    return " ".join(cleaned)
