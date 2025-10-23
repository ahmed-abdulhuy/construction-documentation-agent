
export default function DocumentsTable( { documentProps }) {
    return (
        <div className="overflow-x-auto mt-6">
        <table className="min-w-full text-sm text-left border border-gray-200 rounded-lg">
            <thead className="bg-gray-100 text-gray-700 uppercase text-xs">
            <tr>
                {Object.keys(documentProps).map((col, idx) => (
                <th key={idx} className="px-4 py-3 border-b">
                    {col}
                </th>
                ))}
            </tr>
            </thead>
            <tbody className="bg-white">
            <tr className="hover:bg-gray-50">
                {Object.values(documentProps).map((col, idx) => (
                <td key={idx} className="px-4 py-2 border-b">
                    {col}
                </td>
                ))}
            </tr>
            </tbody>
        </table>
        </div>
    )
}