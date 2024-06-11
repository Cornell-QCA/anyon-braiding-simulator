use pyo3::prelude::*;
use pyo3::types::PyAny;

/// Different Anyon models that can be used to simulate the system
#[pyclass]
pub enum AnyonModel {
    Ising,
    Fibonacci,
    Custom,
}

impl<'a> FromPyObject<'a> for AnyonModel {
    fn extract(obj: &'a PyAny) -> PyResult<Self> {
        // Example:
        // Ok(AnyonModel { field: obj.getattr("field")?.extract()? })
        unimplemented!()
    }
}

#[pymethods]
impl AnyonModel {
    #[new]
    fn new() -> Self {
        AnyonModel::Ising
    }
}

/// The parameters accompanying a model
#[pyclass]
pub struct Model {
    model_type: AnyonModel,
    // more fields which we'll impl later
}

#[pymethods]
impl Model {
    #[new]
    fn new(model_type: AnyonModel) -> Self {
        Model { model_type }
    }
}
