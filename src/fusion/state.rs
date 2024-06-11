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

        self.anyons.push(anyon);
        Ok(true)
    }

    /// Verify the operation
    fn verify_operation(&self, time:u32, operation: FusionPair) -> bool {
        let mut fusible_anyons: Vec<bool>;
        for i in 1..self.anyons.len(){
           fusible_anyons.push(true)
        } 
        for (t, op) in self.operations{
            
            fusible_anyons[op.anyon_2()] = false;
            if t == time{
                fusible_anyons[op.anyon_1()] = false;
            }
        }
        for i in operation.anyon_1()+1..operation.anyon_2()-1{
            if fusible_anyons[i]{
                return false
            }
    
        }
        true

    }

    /// Add an operation to the state
    fn add_operation(&mut self, time: u32, operation: FusionPair) -> PyResult<(bool)> {
        let result  = Self::verify_operation(self, time, operation);
        if !result{
            return Ok(false);
        }
        self.operations.push((time, operation));

        Ok(true)
    }



}
