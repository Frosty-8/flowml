use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use csv::{ReaderBuilder, WriterBuilder};
use rayon::prelude::*;

#[pyfunction]
pub fn drop_nulls(input_path: String, output_path: String) -> PyResult<usize> {
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&input_path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let headers = rdr.headers()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?
        .clone();

    // 🔥 Load all records
    let records: Vec<_> = rdr.records()
        .filter_map(Result::ok)
        .collect();

    // 🔥 Parallel filtering
    let filtered: Vec<_> = records
        .par_iter()
        .filter(|record| record.iter().all(|f| !f.trim().is_empty()))
        .cloned()
        .collect();

    let mut wtr = WriterBuilder::new()
        .from_path(&output_path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    wtr.write_record(&headers)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    for record in &filtered {
        wtr.write_record(record)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    }

    wtr.flush()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    Ok(filtered.len())
}


#[pyfunction]
pub fn fill_nulls(input_path: String, output_path: String, fill_value: String) -> PyResult<()> {
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_path(&input_path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let headers = rdr.headers()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?
        .clone();

    let records: Vec<_> = rdr.records()
        .filter_map(Result::ok)
        .collect();

    // 🔥 Parallel fill
    let filled: Vec<Vec<String>> = records
        .par_iter()
        .map(|record| {
            record.iter()
                .map(|v| {
                    if v.trim().is_empty() {
                        fill_value.clone()
                    } else {
                        v.to_string()
                    }
                })
                .collect()
        })
        .collect();

    let mut wtr = WriterBuilder::new()
        .from_path(&output_path)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    wtr.write_record(&headers)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    for row in filled {
        wtr.write_record(&row)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    }

    wtr.flush()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    Ok(())
}