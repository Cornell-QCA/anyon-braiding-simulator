use pyo3::prelude::*;

// use super::anyon::{Anyon, IsingTopoCharge};

/// Different Anyon models that can be used to simulate the system
#[pyclass]
#[derive(PartialEq, Eq)]
pub enum AnyonModel {
    Ising,
    Fibonacci,
    Custom,
}

#[pymethods]
impl AnyonModel {
    #[new]
    fn new() -> Self {
        AnyonModel::Ising
    }
}

// Commenting out Model for now because it has no use atm We might port the
// python stuff to rust later, but for now we have no use

/// The parameters accompanying a model
/// More docs later when we impl stuff from python
#[pyclass]
pub struct Model {
    model_type: AnyonModel,
    // more fields which we'll impl later
}

#[pymethods]
impl Model {
    #[new]
    fn new() -> Self {
        // Model { model_type }
        Model {
            model_type: AnyonModel::Ising,
        }
    }

}
