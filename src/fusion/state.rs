use pyo3::prelude::*;
use crate::{
    fusion::fusion::FusionPair,
    model::anyon::Anyon,
};

/// The state of the system
#[pyclass]
struct State {
    anyons: Vec<Anyon>,
    operations: Vec<(u32, FusionPair)>,
}

#[pymethods]
pub impl State {
    #[new]
    fn new() -> Self {
        State {
            anyons: Vec::new(),
            operations: Vec::new(),
        }
    }

    /// Add an anyon to the state
    fn add_anyon(&mut self, anyon: Anyon) -> PyResult<(bool)> {
        Ok((True))
    }

    /// Add an operation to the state
    fn add_operation(&mut self, time: u32, operation: FusionPair) -> PyResult<(bool)> {
        Ok((True))
    }

    /// Verify the operation
    fn verify_operation() -> bool {
        true
    }

}
