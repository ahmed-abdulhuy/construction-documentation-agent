'use client';
import { useState, useEffect } from 'react';
import DocumentView from './components/document-view/document-view';
import { fetchedDocumentsProcess } from '@/utilities';

export default function Home() {
  const [documentList, setDocumentList] = useState([]);
  const [loading, setLoading] = useState(true);

    useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const res = await fetch("http://localhost:8000/documents/BRF-001");
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
    <>
      {documentList.map((document, index) => {
        return (
        <DocumentView key={index} documentProps={document} />
      )})}
    </>   
  );
}
