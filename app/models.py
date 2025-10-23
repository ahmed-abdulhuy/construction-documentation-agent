from pydantic import BaseModel

from typing import List, Optional, Dict

class Document(BaseModel):
    id: str
    text: str
    metadata: Optional[Dict] = {}

class AddDocumentsRequest(BaseModel):
    documents: List[Document]

class QueryRequest(BaseModel):
    queryTexts: List[str]
    nResults: Optional[int] = 5

class UpdateDocumentRequest(BaseModel):
    id: str
    newText: Optional[str] = None
    newMetadata: Optional[Dict] = None

class DeleteRequest(BaseModel):
    ids: List[str]
