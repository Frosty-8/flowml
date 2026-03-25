import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import DashboardLayout from "./layout/DashboardLayout";

import Upload from "./pages/Upload";
import Preview from "./pages/Preview";
import Pipeline from "./pages/Pipeline";
import Metrics from "./pages/Metrics";

function AnimatedRoutes() {
    const location = useLocation();

    return (
        <AnimatePresence mode="wait">
            <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.25 }}
            >
                <Routes location={location}>
                    <Route path="/" element={<Upload />} />
                    <Route path="/preview" element={<Preview />} />
                    <Route path="/pipeline" element={<Pipeline />} />
                    <Route path="/metrics" element={<Metrics />} />
                </Routes>
            </motion.div>
        </AnimatePresence>
    );
}

function App() {
    return (
        <BrowserRouter>
            <DashboardLayout>
                <AnimatedRoutes />
            </DashboardLayout>
        </BrowserRouter>
    );
}

export default App;