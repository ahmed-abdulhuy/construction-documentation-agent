import { fetchedDocumentsProcess, queriedDocumentsProcess } from "@/utilities";
import { useState } from "react";


/**
 * Submit a prompt, fetch the response from the server, and set the document list state.
 * @param {(setDocumentList: Function) => void} setDocumentList - Function to set the document list state.
 * @returns {Promise<void>}
 */
export default function PromptBar({ setDocumentList }) {
    const [prompt, setPrompt] = useState('');
    const nResults = 3;

    // fetch the response from the server and set the response state
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch("http://localhost:8000/documents/query", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                queryTexts: [prompt],
                nResults: nResults,
            }),
        });
        const data = await res.json();
        console.log("Prompt response data:", data);
        const documentList = queriedDocumentsProcess(data.documents);
        console.log("Prompt response document list:", documentList);
        setDocumentList(documentList);
    };

    return (
        <div className="w-full flex justify-center items-center gap my-4">
            <form 
                onSubmit={handleSubmit} 
                className="w-[100%] flex items center gap-2 bg-white">
                <input
                    className="flex-grow border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus-ring-blue-500"
                    type="text"
                    value={prompt} 
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter prompt"
                />
                <button 
                    type="submit" 
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                    >Send</button>
            </form>
        </div>
        
    );
}
