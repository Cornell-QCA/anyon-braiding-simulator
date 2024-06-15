use std::slice::SliceIndex;

use pyo3::prelude::*;

/// Lazy solution for now, will properly implement a more general Topo Charge w/ specified
/// version for each different model
#[pyclass]
#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
pub enum IsingTopoCharge {
    Psi,
    Vacuum,
    Sigma,
}

impl IsingTopoCharge {
    pub fn value(&self) -> usize {
        match self {
            IsingTopoCharge::Psi => 0,
            IsingTopoCharge::Vacuum => 1,
            IsingTopoCharge::Sigma => 2,
        }
    }
}

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct Anyon {
    #[pyo3(get)]
    name: String,
    #[pyo3(get)]
    charge: IsingTopoCharge,
    #[pyo3(get)]
    position: (f64, f64),
}

pub trait AccessAnyon {
    fn name(&self) -> &str;
    fn charge(&self) -> IsingTopoCharge;
    fn position(&self) -> (f64, f64);
}

impl AccessAnyon for Anyon {
    fn name(&self) -> &str {
        &self.name
    }

    fn charge(&self) -> IsingTopoCharge {
        self.charge.clone()
    }

    fn position(&self) -> (f64, f64) {
        self.position
    }
}


#[pymethods]
impl Anyon {
    #[new]
    pub fn new(name: String, charge: IsingTopoCharge, position: (f64, f64)) -> Self {
        Anyon {
            name,
            charge,
            position,
        }
    }
}
