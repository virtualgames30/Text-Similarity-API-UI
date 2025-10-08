# similarity_engine.py

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load semantic model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def tfidf_similarity(text1, text2):
    logger.info("Running TF-IDF similarity")
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(float(similarity), 4)

def semantic_similarity(text1, text2):
    logger.info("Running Semantic similarity (BERT)")
    embeddings = model.encode([text1, text2], normalize_embeddings=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(float(similarity), 4)

def compute_similarity(text1, text2, method="tfidf"):
    logger.info(f"Computing similarity using method: {method}")
    if method == "tfidf":
        return {"method": "TF-IDF", "score": tfidf_similarity(text1, text2)}
    elif method == "semantic":
        return {"method": "Semantic (BERT)", "score": semantic_similarity(text1, text2)}
    else:
        raise ValueError("Invalid method. Choose 'tfidf' or 'semantic'.")
