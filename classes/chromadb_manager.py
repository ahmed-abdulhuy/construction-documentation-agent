import chromadb


class ChromaDBManager:
    def __init__(self, dbPath: str = "chromadb_store", collectionName="materials_log"):
        """
        Initialize the ChromaDB client and collection.
        """
        self.client = chromadb.PersistentClient(path=dbPath)

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collectionName,
        )


    # CREATE 
    def addDocuments(self, ids: list, texts: list, metadatas: list):
        """
        Add documents with embeddings and metadata.
        """
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        print(f"Added {len(ids)} documents.")


    # READ 
    def query(self, queryTexts: list, nResults: int = 5):
        """
        Query the collection by text similarity.
        """
        results = self.collection.query(
            query_texts=queryTexts,
            n_results=nResults
        )
        return results


    def getByID(self, ids: list):
        """
        Retrieve documents by their IDs.
        """
        results = self.collection.get(ids=ids)
        return results


    # UPDATE 
    def updateDocument(self, id: str, newText: str = None, newMetadata: dict = None):
        """
        Update the text or metadata of a single document.
        """
        if newText is not None:
            self.collection.update(ids=[id], documents=[newText])
        if newMetadata is not None:
            self.collection.update(ids=[id], metadatas=[newMetadata])
        print(f"Updated document {id}.")


    # DELETE 
    def deleteDocuments(self, ids: list):
        """
        Delete documents by ID.
        """
        self.collection.delete(ids=ids)
        print(f"Deleted documents: {ids}")
