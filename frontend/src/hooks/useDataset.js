export default function useDataset() {
    const getId = () => {
        return localStorage.getItem("dataset_id");
    };

    const setId = (id) => {
        localStorage.setItem("dataset_id", id);
    };

    const clear = () => {
        localStorage.removeItem("dataset_id");
    };

    return { getId, setId, clear };
}