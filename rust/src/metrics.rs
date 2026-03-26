use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use csv::ReaderBuilder;

#[pyfunction]
pub fn basic_stats(path: String) -> PyResult<(usize, usize)> {
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_path(path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let headers = rdr.headers()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?
        .len();

    let rows = rdr.records().count(); // 🔥 faster

    Ok((rows, headers))
}