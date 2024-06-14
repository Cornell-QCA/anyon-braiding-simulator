use crate::{fusion::fusion::AccessFusionPair, fusion::fusion::FusionPair, model::anyon::Anyon};
use pyo3::prelude::*;

/// The state of the system
#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct State {
    #[pyo3(get)]
    anyons: Vec<Anyon>,
    #[pyo3(get)]
    operations: Vec<(u32, FusionPair)>,
}

pub trait AccessState {
    /// Get the anyons in the state
    fn anyons(&self) -> Vec<Anyon>;

    /// Get the operations in the state
    fn operations(&self) -> Vec<(u32, FusionPair)>;
}

impl AccessState for State {
    fn anyons(&self) -> Vec<Anyon> {
        self.anyons.clone()
    }

    fn operations(&self) -> Vec<(u32, FusionPair)> {
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
    /// TODO: Provide better error for panic when no anyons loaded
    fn verify_operation(&self, time: u32, operation: &FusionPair) -> bool {
        assert!(operation.anyon_1() < operation.anyon_2());
        assert!(operation.anyon_2() < self.anyons.len());
        let mut fusible_anyons = vec![true; self.anyons.len()];

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
