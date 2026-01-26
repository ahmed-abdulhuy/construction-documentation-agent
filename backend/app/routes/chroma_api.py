from fastapi import APIRouter, HTTPException
from app.chromaDB_API.models import AddDocumentsRequest, QueryRequest, UpdateDocumentRequest, DeleteRequest
from app.chromaDB_API.chromadb_manager import ChromaDBManager

router = APIRouter(prefix="/documents", tags=["documents"])


# Initialize ChromaDBManager
dbManager = ChromaDBManager(dbPath="./chromadb_store")

# CREATE
@router.post("/add")
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
@router.get("/")
def getAllDocuments():
    results = dbManager.getAllDocuments()
    return results

# READ-QUERY
@router.post("/query")
def queryDocuments(request: QueryRequest):
    results = dbManager.query(request.queryTexts, request.nResults)
    return {
        "message": f"queried documents.",
        "documents": results
    }

# READ-BY ID
@router.get("/{docID}")
def getDocument(docID: str):
    results = dbManager.getByID([docID])
    if not results["documents"]:
        raise HTTPException(status_code=404, detail="Document not found")
    return results

# UPDATE
@router.put("/update")
def updateDocument(request: UpdateDocumentRequest):
    dbManager.updateDocument(request.id, request.newText, request.newMetadata)
    return {
        "message": f"Document {request.id} updated.",
        "documents": dbManager.getByID([request.id])
        }

# DELETE
@router.delete("/documents/delete")
def deleteDocuments(request: DeleteRequest):
    dbManager.deleteDocuments(request.ids)
    return {"message": f"Deleted documents: {request.ids}"}
