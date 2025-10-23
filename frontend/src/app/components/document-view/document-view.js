
export default function DocumentView({ documentProps }) {
    // console.log(documentProps)
    return (
        <>
            <ul className="list-disc list-inside p-4">
            {documentProps && Object.keys(documentProps).map((item, index) => {
                console.log('item:', item, 'value:', documentProps[item]);
                return (
                    <li key={index} className="mb-2">
                        <span className="font-semibold">{item}: </span>
                        {typeof documentProps[item] !== 'object' && (<span>{documentProps[item]}</span>)} 
                    </li>
                )})}
            </ul>
        </>
    );
}