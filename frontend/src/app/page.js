'use client';
import { useState } from 'react';
import PromptBar from './components/prompt-bar/prompt-bar';
import DocumentsTable from './components/documents-table/documents-table';

export default function Home() {
  const [response, setResponse] = useState('');
  
  return (
    <>
      <PromptBar setResponse={setResponse} />
      {
        response && Array.isArray(response) &&
        response.map((document, index) => {
          return (
            <DocumentsTable key={index} documentProps={document}/>        
      )})}
    </>   
  );
}
