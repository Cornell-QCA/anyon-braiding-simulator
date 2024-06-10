use pyo3::prelude::*;
use crate::{
    fusion::fusion::FusionPair,
    model::anyon::Anyon,
};

/// The state of the system
#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct State {
    anyons: Vec<Anyon>,
    operations: Vec<(u32, FusionPair)>,
}

#[pymethods]
impl State {
    #[new]
    fn new() -> Self {
        State {
            anyons: Vec::new(),
            operations: Vec::new(),
        }
    }

    /// Add an anyon to the state
    fn add_anyon(&mut self, anyon: Anyon) -> PyResult<(bool)> {
        Ok((true))
    }

    /// Add an operation to the state
    fn add_operation(&mut self, time: u32, operation: FusionPair) -> PyResult<(bool)> {
        Ok((true))
    }

    /// Verify the operation
    #[staticmethod]
    fn verify_operation() -> bool {
        true
    }

}
