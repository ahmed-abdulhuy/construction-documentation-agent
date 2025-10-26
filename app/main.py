from app.models import AddDocumentsRequest, QueryRequest, UpdateDocumentRequest, DeleteRequest
from fastapi.middleware.cors import CORSMiddleware
from classes.chromadb_manager import ChromaDBManager
from fastapi import FastAPI
from typing import List
import json
import math
import os
import sys
from classes.similarity_check import SimilarityCheck

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


app = FastAPI(title="ChromaDB CRUD API")

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],       # You can restrict this to ['GET', 'POST'] if you want
    allow_headers=["*"],
)


# def sanitize_dict(d):
#     return {
#         k: (None if isinstance(v, float) and math.isnan(v) else v)
#         for k, v in d.items()
#     }


# rag = SimilarityCheck()
 
# @app.get("/")
# async def read_root(query: str = ''):
#     cosineSimilarity = rag.checkSimilarity(query)
#     cosineSimilarity = [sanitize_dict(item) for item in cosineSimilarity]
#     return json.dumps(cosineSimilarity)




# Initialize ChromaDBManager
dbManager = ChromaDBManager(dbPath="./chromadb_store")

# CREATE
@app.post("/documents/add")
def addDocuments(request: AddDocumentsRequest):
    ids = [doc.id for doc in request.documents]
    texts = [doc.text for doc in request.documents]
    metadatas = [doc.metadata for doc in request.documents]

    dbManager.addDocuments(ids, texts, metadatas)
    return {
        "message": f"Added {len(ids)} documents.",
        "documents": dbManager.getByID(ids)
        }

# READ-ALL
@app.get("/documents/")
def getAllDocuments():
    results = dbManager.getAllDocuments()
    return results

# READ-QUERY
@app.post("/documents/query")
def queryDocuments(request: QueryRequest):
    results = dbManager.query(request.queryTexts, request.nResults)
    return {
        "message": f"queried documents.",
        "documents": results
    }

# READ-BY ID
@app.get("/documents/{docID}")
def getDocument(docID: str):
    results = dbManager.getByID([docID])
    if not results["documents"]:
        raise HTTPException(status_code=404, detail="Document not found")
    return results

# UPDATE
@app.put("/documents/update")
def updateDocument(request: UpdateDocumentRequest):
    dbManager.updateDocument(request.id, request.newText, request.newMetadata)
    return {
        "message": f"Document {request.id} updated.",
        "documents": dbManager.getByID([request.id])
        }

# DELETE
@app.delete("/documents/delete")
def deleteDocuments(request: DeleteRequest):
    dbManager.deleteDocuments(request.ids)
    return {"message": f"Deleted documents: {request.ids}"}
