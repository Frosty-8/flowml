use pyo3::prelude::*;

mod csv_reader;
mod cleaning;
mod metrics;
mod batching;

#[pymodule]
fn rust_core(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // CSV
    m.add_function(wrap_pyfunction!(csv_reader::count_rows, m)?)?;
    m.add_function(wrap_pyfunction!(csv_reader::get_headers, m)?)?;

    // Cleaning
    m.add_function(wrap_pyfunction!(cleaning::drop_nulls, m)?)?;
    m.add_function(wrap_pyfunction!(cleaning::fill_nulls, m)?)?;

    // Metrics
    m.add_function(wrap_pyfunction!(metrics::basic_stats, m)?)?;

    Ok(())
}