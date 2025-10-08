from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Traditional TF-IDF similarity
def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(float(similarity), 4)

# Semantic similarity (optional)
def semantic_similarity(text1, text2):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([text1, text2])
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(float(similarity), 4)

# Combined engine
def compute_similarity(text1, text2, method="tfidf"):
    if method == "tfidf":
        return {"method": "TF-IDF", "score": tfidf_similarity(text1, text2)}
    elif method == "semantic":
        return {"method": "Semantic (BERT)", "score": semantic_similarity(text1, text2)}
    else:
        raise ValueError("Invalid method. Choose 'tfidf' or 'semantic'.")
