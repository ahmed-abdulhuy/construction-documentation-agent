import { useState } from "react";


/**
 * Submit a prompt, fetch the response from the server, and set the response state.
 * @param {(response: string) => void} setResponse - Function to set the response state
 * @returns {Promise<void>}
 */
export default function PromptBar(setResponse) {
    const [prompt, setPrompt] = useState('');

    // fetch the response from the server and set the response state
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch(`http://localhost:8000/?query=${encodeURIComponent(prompt)}`);
        const data = await res.json();
        setResponse(JSON.parse(data[0]));
    };

    return (
        <div className="w-full flex justify-center items-center p-4">
            <form 
                onSubmit={handleSubmit} 
                className="w-[85%] flex items center gap-2 p-4p bg-white">
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
