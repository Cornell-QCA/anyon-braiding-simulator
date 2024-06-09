use pyo3::prelude::*;
use crate::fusion::state::State;

#[pyclass]
struct FusionPair {
    anyon_1: u32,
    anyon_2: u32,
}

#[pyclass]
struct Fusion {
    state: State,
}

impl Fusion {
    fn verify_fusion_pair(&self, anyon_1: u32, anyon_2: u32) -> bool {
        true
    }
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
    }
}
