import { useEffect, useState } from "react";
import API from "../api/client";
import useDataset from "../hooks/useDataset";
import Loader from "../components/Loader";
import Table from "../components/Table";
import toast from "react-hot-toast";

export default function Preview() {
    const [data, setData] = useState(null);
    const { getId } = useDataset();

    useEffect(() => {
        const dataset_id = getId();

        if (!dataset_id) {
            toast.error("No dataset found. Please upload first.");
            return;
        }

        API.get(`/preview/?dataset_id=${dataset_id}`)
            .then((res) => {
                setData(res.data);
            })
            .catch((err) => {
                console.error(err);
                toast.error("Preview failed ❌");
            });
    }, []);

    if (!data) return <Loader />;

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Data Preview</h1>

            <div className="bg-gray-900 p-4 rounded-xl border border-gray-800">
                <Table columns={data.columns} data={data.preview} />
            </div>
        </div>
    );
}