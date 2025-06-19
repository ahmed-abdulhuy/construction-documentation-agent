import json
import math
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from classes.similarity_check import SimilarityCheck

app = FastAPI()

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],                      # You can restrict this to ['GET', 'POST'] if you want
    allow_headers=["*"],
)

def sanitize_dict(d):
    return {
        k: (None if isinstance(v, float) and math.isnan(v) else v)
        for k, v in d.items()
    }


rag = SimilarityCheck()
 
@app.get("/")
async def read_root(query: str = ''):
    cosineSimilarity = rag.checkSimilarity(query)
    cosineSimilarity = [sanitize_dict(item) for item in cosineSimilarity]
    return json.dumps(cosineSimilarity), 