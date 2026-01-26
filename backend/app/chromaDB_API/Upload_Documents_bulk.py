import json
import requests


def readJsonFile(filePath):
    with open(filePath, 'r') as file:
        data = json.load(file)
    return data


def processDocuments(documents):
    processedDocuments = []
    for document in documents:
        docID = document.pop("Document_ID")
        text = document.pop("Document Description")
        metaData = document  # Remaining fields as metadata
        processedDoc = {
            "id": docID,
            "text": text,
            "metadata": metaData
        }
        processedDocuments.append(processedDoc)

    return processedDocuments


if __name__ == "__main__":
    # Example usage
    documentsFilePath = "Cleaned-Log.json"
    documentsList = readJsonFile(documentsFilePath)
    processedDocumentList = processDocuments(documentsList)
    print(processedDocumentList)
    url = "http://localhost:8000/documents/add"
    response = requests.post(url, json={"documents": processedDocumentList})

