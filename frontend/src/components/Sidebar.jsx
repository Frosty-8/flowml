import { motion } from "framer-motion";
import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
    const location = useLocation();

    const nav = [
        { name: "Upload", path: "/" },
        { name: "Preview", path: "/preview" },
        { name: "Pipeline", path: "/pipeline" },
        { name: "Metrics", path: "/metrics" }
    ];

    return (
        <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="w-64 bg-gray-900 border-r border-gray-800 p-5"
        >
            <h1 className="text-xl font-bold mb-8 text-white">FlowML</h1>

            <div className="space-y-2">
                {nav.map(item => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`block px-3 py-2 rounded-lg transition ${
                            location.pathname === item.path
                                ? "bg-blue-600 text-white"
                                : "hover:bg-gray-800 text-gray-300"
                        }`}
                    >
                        {item.name}
                    </Link>
                ))}
            </div>
        </motion.div>
    );
}