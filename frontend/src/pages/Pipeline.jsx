import { useState } from "react";
import API from "../api/client";
import useDataset from "../hooks/useDataset";
import toast from "react-hot-toast";

export default function Pipeline() {
    const [result, setResult] = useState(null);
    const [progress, setProgress] = useState(0);
    const [currentStep, setCurrentStep] = useState("");
    const [running, setRunning] = useState(false);

    const { getId } = useDataset();

    const steps = [
        { id: "fill_nulls" },
        { id: "drop_nulls" },
        { id: "summary" }
    ];

    const runPipeline = async () => {
        const dataset_id = getId();

        if (!dataset_id) {
            toast.error("Upload dataset first");
            return;
        }

        setRunning(true);
        setResult(null);
        setProgress(0);
        setCurrentStep("");

        try {
            const res = await API.post("/pipeline/run", {
                dataset_id,
                steps: steps.map(s => ({ step: s.id }))
            });

            const job_id = res.data.job_id;

            toast.success("Pipeline started 🚀");

            const socket = new WebSocket(`ws://127.0.0.1:8000/ws/job/${job_id}`);

            socket.onmessage = (event) => {
                const job = JSON.parse(event.data);

                setProgress(job.progress || 0);
                setCurrentStep(job.current_step || "");

                if (job.status === "completed") {
                    setResult(job.result);
                    setProgress(100);   // 🔥 ensure UI updates
                    setRunning(false);
                    toast.success("Pipeline completed ✅");
                    socket.close();
                }

                if (job.status === "failed") {
                    setRunning(false);
                    toast.error("Pipeline failed ❌");
                    socket.close();
                }
            };

            socket.onerror = () => {
                toast.error("WebSocket error ❌");
                setRunning(false);
            };

        } catch (err) {
            toast.error("Failed to start pipeline ❌");
            setRunning(false);
        }
    };

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Pipeline</h1>

            <button
                onClick={runPipeline}
                disabled={running}
                className="bg-green-600 px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
                {running ? "Running..." : "Run Pipeline"}
            </button>

            {/* Progress */}
            {running && (
                <div className="mt-6">
                    <div className="w-full bg-gray-800 rounded">
                        <div
                            className="bg-blue-500 h-3 rounded transition-all"
                            style={{ width: `${progress}%` }}
                        />
                    </div>

                    <p className="text-sm mt-2 text-gray-400">
                        {progress}% — {currentStep || "Starting..."}
                    </p>
                </div>
            )}

            {/* Result */}
            {result && (
                <pre className="mt-6 bg-gray-900 p-4 rounded-xl text-sm overflow-auto">
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}
        </div>
    );
}