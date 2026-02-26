from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

class MatchRequest(BaseModel):
    job_text: str
    candidate_text: str

@app.post("/jd-match")
def jd_match(data: MatchRequest):
    job_emb = model.encode(data.job_text, convert_to_tensor=True)
    cand_emb = model.encode(data.candidate_text, convert_to_tensor=True)

    similarity = util.cos_sim(job_emb, cand_emb).item()

    if similarity < 0.35:
        score = 0.0
    else:
        score = similarity * 4
        score = min(score, 4.0)

    return {
        "similarity": round(similarity, 3),
        "score": round(score, 2)
    }