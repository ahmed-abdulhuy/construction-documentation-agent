import { useState } from 'react';
import { fetchedDocumentsProcess } from '@/app/utils/utilities';


// API Call for adding a document
async function addDocumentAPI(docID, docText, docMetadata) {
    try {
        const response = await fetch('http://localhost:8000/documents/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "documents": [{
                    id: docID,
                    text: docText,
                    metadata: docMetadata,
                }],
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Document added successfully:', data.documents);
        return data.documents;
    } catch (error) {
        console.error('Error adding document:', error);
        throw error;
    }
}


async function updateDocumentAPI(docID, docText, docMetadata) {
    try {
        const response = await fetch('http://localhost:8000/documents/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: docID,
                newText: docText,
                newMetadata: docMetadata,
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Document updated successfully:', data.documents);
        return data.documents;
    } catch (error) {
        console.error('Error updating document:', error);
        throw error;
    }
}


export default function AddDocument({ documentList, setDocumentList }) {
    // console.log("Document List in AddDocument:", documentList);
    const [docID, setDocID] = useState("");
    const [docText, setDocText] = useState("");
    const [docSource, setDocSource] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        if (docID.trim()) {
            if(documentList.some(doc => doc.ids === docID)) {
                const data = await updateDocumentAPI(docID, docText, { source: docSource });
                const updatedDocuments = fetchedDocumentsProcess(data);
                console.log("Updated Documents:", updatedDocuments);
                setDocumentList(prevList => {
                    // console.log("Previous Document List:", prevList);
                    const filteredList = prevList.filter(doc => doc.ids !== docID);
                    console.log("Filtered Document List:", filteredList);
                    return [...filteredList, ...updatedDocuments];
                });
            } else {
                const data = await addDocumentAPI(docID, docText, { source: docSource });
                const addedDocuments = fetchedDocumentsProcess(data);
                setDocumentList([...documentList, ...addedDocuments]);
            }
            setDocID("");
            setDocText("");
            setDocSource("");
        }
    }


    return (
        <div className='p-4 border border-gray-300  flex flex-col'>
            <form onSubmit={handleSubmit} className='gap-4 align-left'>
                <div>
                    <label htmlFor="docID">Document ID:</label>
                    <input 
                        className='ml-4 border border-grey-300'
                        type="text"
                        placeholder='Document ID'
                        onChange={(e) => setDocID(e.target.value)} 
                        value={docID} />
                </div>

                <div>
                    <label htmlFor="docText" >Document Text:</label>
                    <input 
                        className='ml-4 border border-grey-300'
                        type="text"
                        placeholder='Document Text'
                        onChange={(e) => setDocText(e.target.value)} 
                        value={docText} 
                    />
                </div>

                <div>
                    <label htmlFor="docSource" >Document Source:</label>
                    <input 
                        className='ml-4 border border-grey-300'
                        type="text"
                        placeholder='Document Source'
                        onChange={(e) => setDocSource(e.target.value)} 
                        value={docSource} 
                    />
                </div>

                <div>
                    <button type="submit" className='hover:cursor-pointer hover:bg-blue-400 text-white bg-blue-500 p-2 '>Create</button>
                </div>
            </form>

        </div>
    )
}


// "id": "BRF-002",
// "text": "Wed, 21 Oct 2015 18:27:50 GMT",
// "metadata": {"source": "sample"}