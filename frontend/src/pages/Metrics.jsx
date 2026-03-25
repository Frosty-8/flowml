import { useEffect, useState } from "react";
import Card from "../components/Card";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";

export default function Metrics() {
    const [metrics, setMetrics] = useState(null);
    const [history, setHistory] = useState([]);
    const [jobs, setJobs] = useState({});

    // -----------------------------
    // WebSocket for Metrics
    // -----------------------------
    useEffect(() => {
        const socket = new WebSocket("ws://127.0.0.1:8000/ws/metrics");

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            setMetrics(data);

            setHistory(prev => [
                ...prev.slice(-20),
                {
                    time: new Date().toLocaleTimeString(),
                    requests: data.requests.total_requests
                }
            ]);
        };

        socket.onerror = () => {
            console.error("Metrics socket error");
        };

        return () => socket.close();
    }, []);

    // -----------------------------
    // Fetch Jobs (multi-job dashboard)
    // -----------------------------
    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const res = await fetch("http://127.0.0.1:8000/jobs/");
                const data = await res.json();
                setJobs(data);
            } catch (err) {
                console.error("Failed to fetch jobs");
            }
        };

        fetchJobs();
        const interval = setInterval(fetchJobs, 2000);

        return () => clearInterval(interval);
    }, []);

    if (!metrics) return <p>Loading...</p>;

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Analytics Dashboard</h1>

            {/* KPI Cards */}
            <div className="grid grid-cols-3 gap-6 mb-6">
                <Card title="Requests" value={metrics.requests.total_requests} />
                <Card title="Errors" value={metrics.requests.errors} />
                <Card title="Latency" value={metrics.requests.avg_latency} />
            </div>

            {/* Chart */}
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 mb-6">
                <h2 className="mb-4 text-lg">Request Trend</h2>

                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={history}>
                        <XAxis dataKey="time" />
                        <YAxis />
                        <Tooltip />
                        <Line
                            type="monotone"
                            dataKey="requests"
                            stroke="#3b82f6"
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* Multi-job dashboard */}
            <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
                <h2 className="mb-4 text-lg">Jobs</h2>

                <div className="space-y-2 text-sm">
                    {Object.keys(jobs).length === 0 && (
                        <p className="text-gray-400">No jobs yet</p>
                    )}

                    {Object.entries(jobs).map(([id, job]) => (
                        <div
                            key={id}
                            className="flex justify-between bg-gray-800 px-3 py-2 rounded"
                        >
                            <span>{id.slice(0, 6)}</span>
                            <span>{job.status}</span>
                            <span>{job.progress}%</span>
                            <span className="text-gray-400">
                                {job.step || "-"}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}