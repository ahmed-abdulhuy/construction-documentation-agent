
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
                        {typeof documentProps[item] !== 'object' ? (<span>{documentProps[item]}</span>) : 
                            <ul className="list-[square] list-inside pl-8">
                                {
                                    documentProps[item] && Object.keys(documentProps[item]).map((subItem, subIndex) => (
                                        <li key={`${index}-${subIndex}`} className="mb-2">
                                                <span className="font-semibold">{subItem}: </span>
                                                <span>{documentProps[item][subItem]}</span>
                                        </li>
                                ))}
                            </ul>
                        } 
                    </li>
                )})}
            </ul>
        </>
    );
}