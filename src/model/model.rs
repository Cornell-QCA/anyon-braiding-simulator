use pyo3::prelude::*;

use super::anyon::{AccessAnyon, Anyon, IsingTopoCharge};

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

/// The parameters accompanying a model
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
