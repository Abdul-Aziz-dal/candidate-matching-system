from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

vectorizer = TfidfVectorizer()

class MatchRequest(BaseModel):
    job_text: str
    candidate_text: str

@app.post("/jd-match")
def jd_match(data: MatchRequest):
    texts = [data.job_text, data.candidate_text]
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    if similarity < 0.35:
        score = 0.0
    else:
        score = min(similarity * 4, 4.0)

    return {
        "similarity": round(float(similarity), 3),
        "score": round(float(score), 2)
    }