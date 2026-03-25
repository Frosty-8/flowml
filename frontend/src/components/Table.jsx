export default function Table({ columns, data }) {
    return (
        <table className="w-full border">
            <thead className="bg-gray-100">
                <tr>
                    {columns.map((col, i) => (
                        <th key={i} className="p-2 border">{col}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {data.map((row, i) => (
                    <tr key={i}>
                        {Object.values(row).map((val, j) => (
                            <td key={j} className="p-2 border">
                                {val ?? "-"}
                            </td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
}