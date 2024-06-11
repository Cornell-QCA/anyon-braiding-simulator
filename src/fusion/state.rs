use crate::{fusion::fusion::FusionPair, model::anyon::Anyon};
use pyo3::prelude::*;

/// The state of the system
#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct State {
    anyons: Vec<Anyon>,
    operations: Vec<(u32, FusionPair)>,
}

pub trait AccessState {
    /// Get the anyons in the state
    fn get_anyons(&self) -> Vec<Anyon>;

    /// Get the operations in the state
    fn get_operations(&self) -> Vec<(u32, FusionPair)>;
}

impl AccessState for State {
    fn get_anyons(&self) -> Vec<Anyon> {
        self.anyons.clone()
    }

    fn get_operations(&self) -> Vec<(u32, FusionPair)> {
        self.operations.clone()
    }
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
    fn add_anyon(&mut self, anyon: Anyon) -> PyResult<bool> {
        self.anyons.push(anyon);
        Ok(true)
    }

    /// Verify the operation
    fn verify_operation(&self, time: u32, operation: &FusionPair) -> bool {
        let mut fusible_anyons = vec![true; self.anyons.len() - 1];

        for (t, op) in &self.operations {
            fusible_anyons[op.anyon_2()] = false;
            if *t == time {
                fusible_anyons[op.anyon_1()] = false;
            }
        }

        if !fusible_anyons[operation.anyon_1()] || !fusible_anyons[operation.anyon_2()] {
            return false;
        }

        for i in operation.anyon_1() + 1..operation.anyon_2() - 1 {
            if fusible_anyons[i] {
                return false;
            }
        }
        true
    }

    /// Add an operation to the state
    fn add_operation(&mut self, time: u32, operation: FusionPair) -> PyResult<bool> {
        let result = Self::verify_operation(self, time, &operation);
        if !result {
            return Ok(false);
        }
        self.operations.push((time, operation));

        Ok(true)
    }
}
