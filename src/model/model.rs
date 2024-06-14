use pyo3::prelude::*;

use super::anyon::{AccessAnyon, Anyon, IsingTopoCharge};

/// Different Anyon models that can be used to simulate the system
#[pyclass]
#[derive(PartialEq, Eq)]
pub enum AnyonModel {
    Ising,
    Fibonacci,
    Custom,
}

#[pymethods]
impl AnyonModel {
    #[new]
    fn new() -> Self {
        AnyonModel::Ising
    }
}

/// The parameters accompanying a model
#[pyclass]
pub struct Model {
    model_type: AnyonModel,
    // more fields which we'll impl later
}

#[pymethods]
impl Model {
    #[new]
    fn new() -> Self {
        // Model { model_type }
        Model {
            model_type: AnyonModel::Ising,
        }
    }

    /// Fuses anyons according to their fusion rules
    pub fn apply_fusion(&self, anyon_1: Anyon, anyon_2: Anyon) -> Vec<Anyon> {
        if self.model_type == AnyonModel::Ising {
            match (anyon_1.charge(), anyon_2.charge()) {
                (IsingTopoCharge::Vacuum, IsingTopoCharge::Vacuum) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Vacuum,
                        (0.0, 0.0),
                    )]
                }
                (IsingTopoCharge::Sigma, IsingTopoCharge::Sigma) => {
                    vec![
                        Anyon::new(
                            format!("{}_{}", anyon_1.name(), anyon_2.name()),
                            IsingTopoCharge::Vacuum,
                            (0.0, 0.0),
                        ),
                        Anyon::new(
                            format!("{}_{}", anyon_1.name(), anyon_2.name()),
                            IsingTopoCharge::Psi,
                            (0.0, 0.0),
                        ),
                    ]
                }
                (IsingTopoCharge::Psi, IsingTopoCharge::Psi) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Vacuum,
                        (0.0, 0.0),
                    )]
                }

                (IsingTopoCharge::Vacuum, IsingTopoCharge::Sigma) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Sigma,
                        (0.0, 0.0),
                    )]
                }
                (IsingTopoCharge::Sigma, IsingTopoCharge::Vacuum) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Sigma,
                        (0.0, 0.0),
                    )]
                }

                (IsingTopoCharge::Vacuum, IsingTopoCharge::Psi) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Psi,
                        (0.0, 0.0),
                    )]
                }
                (IsingTopoCharge::Psi, IsingTopoCharge::Vacuum) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Psi,
                        (0.0, 0.0),
                    )]
                }

                (IsingTopoCharge::Sigma, IsingTopoCharge::Psi) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Sigma,
                        (0.0, 0.0),
                    )]
                }
                (IsingTopoCharge::Psi, IsingTopoCharge::Sigma) => {
                    vec![Anyon::new(
                        format!("{}_{}", anyon_1.name(), anyon_2.name()),
                        IsingTopoCharge::Sigma,
                        (0.0, 0.0),
                    )]
                }
                _ => Vec::new(),
            }
        } else {
            unimplemented!()
        }
    }
}
