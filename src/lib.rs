use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use rtoon::{
    encode_default as rtoon_encode_default,
    decode_default as rtoon_decode_default,
    encode as rtoon_encode,
    decode as rtoon_decode,
    EncodeOptions as RtoonEncodeOptions,
    DecodeOptions as RtoonDecodeOptions,
    Delimiter as RtoonDelimiter,
};
use serde_json::json;

/// Delimiter options for encoding TOON format.
#[pyclass]
#[derive(Clone)]
pub struct Delimiter {
    inner: RtoonDelimiter,
}

#[pymethods]
impl Delimiter {
    /// Comma delimiter (default)
    #[staticmethod]
    fn comma() -> Self {
        Self { inner: RtoonDelimiter::Comma }
    }

    /// Pipe delimiter
    #[staticmethod]
    fn pipe() -> Self {
        Self { inner: RtoonDelimiter::Pipe }
    }

    /// Tab delimiter
    #[staticmethod]
    fn tab() -> Self {
        Self { inner: RtoonDelimiter::Tab }
    }
}

/// Options for encoding to TOON format.
#[pyclass]
pub struct EncodeOptions {
    inner: RtoonEncodeOptions,
}

#[pymethods]
impl EncodeOptions {
    /// Create new encoding options with defaults.
    #[new]
    fn new() -> Self {
        Self {
            inner: RtoonEncodeOptions::new(),
        }
    }

    /// Set the delimiter for arrays and inline objects.
    fn with_delimiter(&mut self, delimiter: Delimiter) -> Self {
        Self {
            inner: self.inner.clone().with_delimiter(delimiter.inner),
        }
    }

    /// Set the length marker character for arrays.
    fn with_length_marker(&mut self, marker: char) -> Self {
        Self {
            inner: self.inner.clone().with_length_marker(marker),
        }
    }
}

/// Options for decoding TOON format.
#[pyclass]
pub struct DecodeOptions {
    inner: RtoonDecodeOptions,
}

#[pymethods]
impl DecodeOptions {
    /// Create new decoding options with defaults.
    #[new]
    fn new() -> Self {
        Self {
            inner: RtoonDecodeOptions::new(),
        }
    }

    /// Enable or disable strict mode (validates array lengths).
    fn with_strict(&mut self, strict: bool) -> Self {
        Self {
            inner: self.inner.clone().with_strict(strict),
        }
    }

    /// Enable or disable type coercion.
    fn with_coerce_types(&mut self, coerce: bool) -> Self {
        Self {
            inner: self.inner.clone().with_coerce_types(coerce),
        }
    }
}

#[pyfunction]
fn hello_from_bin() -> String {
    let data = json!({
        "user": {
            "id": 123,
            "name": "Ada",
            "tags": ["reading", "gaming"],
            "active": true
        }
    });

    let toon = rtoon_encode_default(&data).unwrap();
    toon
}

/// Encode a JSON string to TOON format using default options.
///
/// Args:
///     json_str: A JSON string to encode
///
/// Returns:
///     A TOON-formatted string
///
/// Raises:
///     ValueError: If the JSON is invalid or encoding fails
#[pyfunction]
fn encode_default(json_str: &str) -> PyResult<String> {
    let value: serde_json::Value = serde_json::from_str(json_str)
        .map_err(|e| PyValueError::new_err(format!("Invalid JSON: {}", e)))?;

    rtoon_encode_default(&value)
        .map_err(|e| PyValueError::new_err(format!("Encoding failed: {}", e)))
}

/// Decode a TOON string to JSON format using default options.
///
/// Args:
///     toon_str: A TOON-formatted string to decode
///
/// Returns:
///     A JSON string
///
/// Raises:
///     ValueError: If the TOON string is invalid or decoding fails
#[pyfunction]
fn decode_default(toon_str: &str) -> PyResult<String> {
    let value = rtoon_decode_default(toon_str)
        .map_err(|e| PyValueError::new_err(format!("Decoding failed: {}", e)))?;

    serde_json::to_string(&value)
        .map_err(|e| PyValueError::new_err(format!("JSON serialization failed: {}", e)))
}

/// Encode a JSON string to TOON format with custom options.
///
/// Args:
///     json_str: A JSON string to encode
///     options: EncodeOptions for customizing the output format
///
/// Returns:
///     A TOON-formatted string
///
/// Raises:
///     ValueError: If the JSON is invalid or encoding fails
#[pyfunction]
fn encode(json_str: &str, options: &EncodeOptions) -> PyResult<String> {
    let value: serde_json::Value = serde_json::from_str(json_str)
        .map_err(|e| PyValueError::new_err(format!("Invalid JSON: {}", e)))?;

    rtoon_encode(&value, &options.inner)
        .map_err(|e| PyValueError::new_err(format!("Encoding failed: {}", e)))
}

/// Decode a TOON string to JSON format with custom options.
///
/// Args:
///     toon_str: A TOON-formatted string to decode
///     options: DecodeOptions for customizing the decoding behavior
///
/// Returns:
///     A JSON string
///
/// Raises:
///     ValueError: If the TOON string is invalid or decoding fails
#[pyfunction]
fn decode(toon_str: &str, options: &DecodeOptions) -> PyResult<String> {
    let value = rtoon_decode(toon_str, &options.inner)
        .map_err(|e| PyValueError::new_err(format!("Decoding failed: {}", e)))?;

    serde_json::to_string(&value)
        .map_err(|e| PyValueError::new_err(format!("JSON serialization failed: {}", e)))
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_function(wrap_pyfunction!(encode_default, m)?)?;
    m.add_function(wrap_pyfunction!(decode_default, m)?)?;
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    m.add_class::<Delimiter>()?;
    m.add_class::<EncodeOptions>()?;
    m.add_class::<DecodeOptions>()?;
    Ok(())
}
