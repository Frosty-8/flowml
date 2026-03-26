use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use csv::ReaderBuilder;

#[pyfunction]
pub fn count_rows(path: String) -> PyResult<usize> {
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_path(path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    Ok(rdr.records().count()) // 🔥 faster
}

#[pyfunction]
pub fn get_headers(path: String) -> PyResult<Vec<String>> {
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_path(path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let headers = rdr.headers()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    Ok(headers.iter().map(|s| s.to_string()).collect())
}