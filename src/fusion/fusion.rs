use pyo3::prelude::*;
use crate::fusion::state::State;

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct FusionPair {
    anyon_1: usize,
    anyon_2: usize,
}


impl FusionPair{
    pub fn anyon_1(&self) -> usize{
        self.anyon_1
    }
    pub fn anyon_2(&self) -> usize{
        self.anyon_2
    }
}
#[pyclass]
struct Fusion {
    state: State,
}


#[pymethods]
impl Fusion {
    #[new]
    fn new(state: State) -> Self {
        Fusion { state }
    }

    fn all_basis(&self) -> PyResult<Vec<FusionPair>> {
        Ok(Vec::new())
    }

    fn __str__(&self) -> PyResult<String> {
        // Ok(format!("Fusion: {:?}", self.state))
        Ok("Fusion".to_string())
    }
}
