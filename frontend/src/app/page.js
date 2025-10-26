'use client';
import { useState, useEffect } from 'react';
import DocumentView from './components/document-view/document-view';
import AddDocument from './components/add-document/add-document';
import { fetchedDocumentsProcess } from '@/utilities';
import PromptBar from './components/prompt-bar/prompt-bar';

export default function Home() {
  const [documentList, setDocumentList] = useState([]);
  const [loading, setLoading] = useState(true);

    useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const res = await fetch("http://localhost:8000/documents");
        const data = await res.json();
        const processedDocumentList = fetchedDocumentsProcess(data);
        setDocumentList(processedDocumentList);
      } catch (error) {
        console.error("Error fetching documents:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  if (loading) {
    return <p className="text-gray-500 text-center mt-10">Loading...</p>;
  }
  return (
    <div className="min-h-screen p-8 font-roboto ">
      
      <AddDocument setDocumentList={setDocumentList} documentList={documentList} documentProps={document}/>
      <PromptBar setDocumentList={setDocumentList} />      
      {documentList.map((document, index) => (<DocumentView 
                                                key={index} 
                                                documentList={documentList} 
                                                setDocumentList={setDocumentList}
                                                documentProps={document} />))}
    </div>   
  );
}
