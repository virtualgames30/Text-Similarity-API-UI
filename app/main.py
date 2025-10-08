# app.py

from fastapi import FastAPI, UploadFile, Form, HTTPException
from enum import Enum
from app.similarity_engine import compute_similarity
from app.utils import clean_text

class SimilarityMethod(str, Enum):
    tfidf = "tfidf"
    semantic = "semantic"

app = FastAPI(
    title="Text Similarity REST API",
    description="Compare similarity between two texts using TF-IDF or Semantic methods",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to Text Similarity API 🚀"}

@app.post("/compare-texts/")
async def compare_texts(
    text1: str = Form(...),
    text2: str = Form(...),
    method: SimilarityMethod = Form(SimilarityMethod.tfidf)
):
    clean1 = clean_text(text1)
    clean2 = clean_text(text2)
    try:
        result = compute_similarity(clean1, clean2, method)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "similarity_score": result["score"],
        "method_used": result["method"],
        "percentage_similarity": f"{result['score'] * 100:.2f}%"
    }

@app.post("/compare-files/")
async def compare_files(file1: UploadFile, file2: UploadFile, method: SimilarityMethod = Form(SimilarityMethod.tfidf)):
    text1 = (await file1.read()).decode("utf-8")
    text2 = (await file2.read()).decode("utf-8")
    clean1 = clean_text(text1)
    clean2 = clean_text(text2)
    try:
        result = compute_similarity(clean1, clean2, method)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "similarity_score": result["score"],
        "method_used": result["method"],
        "percentage_similarity": f"{result['score'] * 100:.2f}%"
    }
