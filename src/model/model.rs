use pyo3::prelude::*;

// use super::anyon::{Anyon, IsingTopoCharge};

/// Different Anyon models that can be used to simulate the system
#[pyclass]
#[derive(PartialEq, Eq, Clone, Debug)]
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
