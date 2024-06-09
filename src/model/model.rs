use pyo3::prelude::*;

/// Different Anyon models that can be used to simulate the system
#[pyclass]
enum AnyonModel {
    Ising,
    Fibonacci,
    Custom
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
struct Model {
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
