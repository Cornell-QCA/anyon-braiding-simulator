use pyo3::prelude::*;

/// Lazy solution for now, will properly implement a more general Topo Charge w/ specified
/// version for each different model
#[pyclass]
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub enum IsingTopoCharge {
    Vacuum,
    Sigma,
    Psi,
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
    fn get_name(&self) -> String;
    fn get_charge(&self) -> IsingTopoCharge;
    fn get_position(&self) -> (f64, f64);
}

impl AccessAnyon for Anyon {
    fn get_name(&self) -> String {
        self.name.clone()
    }

    fn get_charge(&self) -> IsingTopoCharge {
        self.charge.clone()
    }

    fn get_position(&self) -> (f64, f64) {
        self.position
    }
}

#[pymethods]
impl Anyon {
    #[new]
    fn new(name: String, charge: IsingTopoCharge, position: (f64, f64)) -> Self {
        Anyon {
            name,
            charge,
            position,
        }
    }
}
