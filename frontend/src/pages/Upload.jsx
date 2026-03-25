import { useRef, useState } from "react";
import API from "../api/client";
import useDataset from "../hooks/useDataset";
import toast from "react-hot-toast";

export default function Upload() {
    const [file, setFile] = useState(null);
    const inputRef = useRef();
    const { setId } = useDataset();

    // 🔥 open file picker
    const openFilePicker = () => {
        inputRef.current.click();
    };

    const handleUpload = async () => {
        if (!file) {
            toast.error("Please select a file");
            return;
        }

        try {
            const formData = new FormData();
            formData.append("file", file);

            const res = await API.post("/upload/", formData);

            const dataset_id = res.data.dataset_id;

            setId(dataset_id);

            toast.success("Upload successful 🚀");

            setTimeout(() => {
                window.location.href = "/preview";
            }, 200);

        } catch (err) {
            console.error(err);
            toast.error("Upload failed ❌");
        }
    };

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Upload Dataset</h1>

            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">

                {/* Hidden Input */}
                <input
                    type="file"
                    ref={inputRef}
                    onChange={(e) => setFile(e.target.files[0])}
                    className="hidden"
                />

                {/* Select Button */}
                <button
                    onClick={openFilePicker}
                    className="bg-gray-800 px-4 py-2 rounded-lg mb-4"
                >
                    Choose File
                </button>

                {/* Show Selected File */}
                {file && (
                    <p className="text-sm text-gray-400 mb-4">
                        Selected: {file.name}
                    </p>
                )}

                {/* Upload Button */}
                <button
                    onClick={handleUpload}
                    className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
                >
                    Upload
                </button>

            </div>
        </div>
    );
}