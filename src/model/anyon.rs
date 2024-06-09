use pyo3::prelude::*;

/// Lazy solution for now, will properly implement a more general Topo Charge w/ specified
/// version for each different model
#[pyclass]
enum IsingTopoCharge {
    Vacuum,
    Sigma,
    Psi,
}

#[pyclass]
struct Anyon {
    #[pyo3(get)]
    name: String,
    #[pyo3(get)]
    charge: IsingTopoCharge,
    #[pyo3(get)]
    position: (f64, f64),
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
