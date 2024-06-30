use crate::{fusion::fusion::FusionPair, model::anyon::Anyon, model::model::AnyonModel};
use crate::util::statevec::StateVec;
use pyo3::prelude::*;

/// The state of the system
#[pyclass]
#[derive(Clone, Debug, PartialEq)]
/// Stores the overall state of the system. Use this struct to keep track of any
/// common information throughout the simulation (e.g. anyons, operations,
/// statevector).
pub struct State {
    #[pyo3(get)]
    anyons: Vec<Anyon>,
    #[pyo3(get)]
    operations: Vec<(u32, FusionPair)>,
    #[pyo3(get)]
    anyon_model: AnyonModel,
    #[pyo3(get)]
    state_vec: StateVec,
}

/// Internal Methods
impl State {
    pub fn anyons(&self) -> Vec<Anyon> {
        self.anyons.clone()
    }

    pub fn operations(&self) -> Vec<(u32, FusionPair)> {
        self.operations.clone()
    }

    pub fn anyon_model(&self) -> AnyonModel{
        self.anyon_model.clone()
    }

    /// Verify the operation
    /// TODO: Provide better error for panic when no anyons loaded
    pub fn verify_operation(&self, time: u32, operation: &FusionPair) -> bool {
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
}

/// Python Methods
#[pymethods]
impl State {
    #[new]
    fn new() -> Self {
        State {
            anyons: Vec::new(),
            operations: Vec::new(),
            anyon_model: AnyonModel::Ising, //Assume model is Ising by default
            state_vec: StateVec::new(1, None),
        }
    }

    /// Add an anyon to the state
    fn add_anyon(&mut self, anyon: Anyon) -> PyResult<bool> {
        self.anyons.push(anyon);
        Ok(true)
    }

    /// Verifies and then adds an operation to the state
    fn add_operation(&mut self, time: u32, operation: FusionPair) -> PyResult<bool> {
        let result = Self::verify_operation(self, time, &operation);
        if !result {
            return Ok(false);
        }
        self.operations.push((time, operation));

        Ok(true)
    }
    fn set_anyon_model(&mut self, model:AnyonModel){
        self.anyon_model=model;
    }
}