'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

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
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt"
        />
        <button type="submit">Send</button>
      </form>
      {/* <div>
        {response && (
          <div>
            <h2>Response:</h2>
            <p>{response}</p>
          </div>
        )}
      </div> */}
      {
        response && Array.isArray(response) &&
        response.map((item, index) => {
          return (
          <div key={index} className="overflow-x-auto">
            <table className="min-w-full border border-gray-300">
              <thead className="bg-gray-100">
                <tr>
                  {Object.keys(item).map((col, idx) => (
                    <th key={idx} className="px-4 py-2 border">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr className="hover:bg-gray-50">
                  {Object.values(item).map((col, idx) => (
                    <td key={idx} className="px-4 py-2 border">
                      {col}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        )
        }
         )
      }   
      <br />   
    </div>
  );
}
