import { useState } from "react";


export default function PromptBar(setResponse) {
    const [prompt, setPrompt] = useState('');
    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch(`http://localhost:8000/?query=${encodeURIComponent(prompt)}`);
        const data = await res.json();
        console.log(data);
        console.log('\n');
        console.log(typeof(data[0]));
        console.log('\n');
        console.log(JSON.parse(data[0]));
        setResponse(JSON.parse(data[0]));
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter prompt"
            />
            <button type="submit">Send</button>
        </form>
    );
}
