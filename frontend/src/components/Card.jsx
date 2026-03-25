import { motion } from "framer-motion";

export default function Card({ title, value }) {
    return (
        <motion.div
            whileHover={{ scale: 1.03 }}
            transition={{ type: "spring", stiffness: 200 }}
            className="bg-gray-900 border border-gray-800 p-5 rounded-xl shadow-md hover:shadow-xl"
        >
            <p className="text-gray-400 text-sm">{title}</p>
            <h2 className="text-2xl font-bold text-white mt-2">{value}</h2>
        </motion.div>
    );
}