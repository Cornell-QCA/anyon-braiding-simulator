use pyo3::prelude::*;

#[pyclass]
#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
/// Options for the topological charge for an Ising Model anyon
pub enum IsingTopoCharge {
    Psi,
    Vacuum,
    Sigma,
}

#[pyclass]
#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
/// Options for the topological charge for an Fibonacci Model anyon
pub enum FibonacciTopoCharge {
    Tau,
    Vacuum,
}

#[pyclass]
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
/// Options for the topological charge for an anyon
/// Currently only supports Ising and Fibonacci models
pub struct TopoCharge {
    ising: Option<IsingTopoCharge>,
    fibonacci: Option<FibonacciTopoCharge>,
}

// Implement TryFrom trait to convert from TopoCharge to specific enums
impl TryFrom<&TopoCharge> for IsingTopoCharge {
    type Error = &'static str;

    fn try_from(value: &TopoCharge) -> Result<Self, Self::Error> {
        value.ising.ok_or("Not an IsingTopoCharge")
    }
}

impl TryFrom<&TopoCharge> for FibonacciTopoCharge {
    type Error = &'static str;

    fn try_from(value: &TopoCharge) -> Result<Self, Self::Error> {
        value.fibonacci.ok_or("Not a FibonacciTopoCharge")
    }
}

#[pymethods]
impl TopoCharge {
    #[new]
    pub fn new(ising: Option<IsingTopoCharge>, fibonacci: Option<FibonacciTopoCharge>) -> Self {
        TopoCharge { ising, fibonacci }
    }

    #[staticmethod]
    pub fn from_ising(ising: IsingTopoCharge) -> Self {
        TopoCharge {
            ising: Some(ising),
            fibonacci: None,
        }
    }

    #[staticmethod]
    pub fn from_fibonacci(fibonacci: FibonacciTopoCharge) -> Self {
        TopoCharge {
            ising: None,
            fibonacci: Some(fibonacci),
        }
    }

    pub fn is_ising(&self) -> bool {
        self.ising.is_some()
    }

    pub fn is_fibonacci(&self) -> bool {
        self.fibonacci.is_some()
    }

    pub fn get_ising(&self) -> IsingTopoCharge {
        self.ising.unwrap()
    }

    pub fn get_fibonacci(&self) -> FibonacciTopoCharge {
        self.fibonacci.unwrap()
    }

    pub fn to_string(&self) -> String {
        if let Some(ising) = self.ising {
            format!("{:?}", ising)
        } else if let Some(fibonacci) = self.fibonacci {
            format!("{:?}", fibonacci)
        } else {
            "None".to_string()
        }
    }
}

impl IsingTopoCharge {
    pub fn value(&self) -> usize {
        *self as usize
    }

    pub fn to_string(&self) -> &str {
        match self {
            IsingTopoCharge::Psi => "Psi",
            IsingTopoCharge::Vacuum => "Vacuum",
            IsingTopoCharge::Sigma => "Sigma",
        }
    }
}

impl FibonacciTopoCharge {
    pub fn value(&self) -> usize {
        *self as usize
    }

    pub fn to_string(&self) -> &str {
        match self {
            FibonacciTopoCharge::Tau => "Tau",
            FibonacciTopoCharge::Vacuum => "Vacuum",
        }
    }
}

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
/// In Topological Quantum Computing, anyons are the fundamental quasiparticles
/// which enable the computation. Anyons have an associated topological charge
/// given by the model used. This struct represents an anyon with a name,
/// charge, and position.
pub struct Anyon {
    #[pyo3(get)]
    name: String,
    #[pyo3(get)]
    charge: TopoCharge,
    #[pyo3(get)]
    position: (f64, f64),
}

impl Anyon {
    pub fn name(&self) -> &str {
        &self.name
    }

    pub fn charge(&self) -> TopoCharge {
        self.charge.clone()
    }

    pub fn position(&self) -> (f64, f64) {
        self.position
    }
}

#[pymethods]
impl Anyon {
    #[new]
    pub fn new(name: String, charge: TopoCharge, position: (f64, f64)) -> Self {
        Anyon {
            name,
            charge,
            position,
        }
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Anyon: name={}, charge={}, position={:?}",
            self.name,
            self.charge.to_string(),
            self.position
        ))
    }
}