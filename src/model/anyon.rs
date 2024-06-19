use pyo3::prelude::*;

#[pyclass]
#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
pub enum IsingTopoCharge {
    Psi,
    Vacuum,
    Sigma,
}

#[pyclass]
#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
pub enum FibonacciTopoCharge {
    Tau,
    Vacuum,
}

#[pyclass]
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
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
        // match self {
        //     IsingTopoCharge::Psi => 0,
        //     IsingTopoCharge::Vacuum => 1,
        //     IsingTopoCharge::Sigma => 2,
        // }
<<<<<<< ours
<<<<<<< Updated upstream
<<<<<<< ours
<<<<<<< ours
    }

    pub fn to_string(&self) -> &str {
        match self {
            IsingTopoCharge::Psi => "Psi",
            IsingTopoCharge::Vacuum => "Vacuum",
            IsingTopoCharge::Sigma => "Sigma",
        }
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> Stashed changes
=======
>>>>>>> theirs
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

impl Anyon {
    pub fn name(&self) -> &str {
        &self.name
    }

    pub fn charge(&self) -> IsingTopoCharge {
        self.charge.clone()
    }

    pub fn position(&self) -> (f64, f64) {
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

    fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "Anyon: name={}, charge={}, position={:?}",
            self.name,
            self.charge.to_string(),
            self.position
        ))
    }
}
