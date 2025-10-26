

async function removeDocumentAPI(docID) {
    try {
        const response = await fetch('http://localhost:8000/documents/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "ids": [docID],
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error removing document:', error);
        throw error;
    }
}


export default function DocumentView({ documentProps, documentList, setDocumentList }) {
    function handleDocumentDelete(e, docID) {
        e.preventDefault();
        if (docID.trim()) {
            removeDocumentAPI(docID);
            setDocumentList(documentList.filter(doc => doc.ids !== docID));
        }
    }


    return (
        <div className="flex justify-between border border-gray-300 my-2">
            <ul className="list-disc list-inside p-4">
            {documentProps && Object.keys(documentProps).map((item, index) => {
                // console.log('item:', item, 'value:', documentProps[item]);
                return (
                    <li key={index} className="mb-2">
                        <span className="font-semibold">{item}: </span>
                        {typeof documentProps[item] !== 'object' ? (<span>{documentProps[item]}</span>) : 
                            documentProps[item] && Object.keys(documentProps[item]).map((subItem, subIndex) => (
                                <>
                                    <ul className="list-[square] list-inside pl-8">
                                        <li key={subIndex}>
                                                <span className="font-semibold">{subItem}: </span>
                                                <span>{documentProps[item][subItem]}</span>
                                        </li>
                                    </ul>
                                </>
                            ))
                        } 
                    </li>
                )})}
            </ul>

            <button 
                className="hover:cursor-pointer hover:bg-blue-300 bg-blue-500 text-white p-2 m-2 h-[30%]"
                onClick={(e) => handleDocumentDelete(e, documentProps.ids)}>
                Remove
            </button>

        </div>
    );
}