import re
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def clean_text(text):
    """
    Clean extracted text before RAG pipeline:
    - Remove URLs
    - Remove special characters
    - Remove extra spaces
    - Lowercase
    - Optional: remove stopwords
    """

    text = text.lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s.,;:!?-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    # OPTIONAL: stopword removal
    cleaned = " ".join([word for word in text.split() if word not in stop_words])

    return cleaned
