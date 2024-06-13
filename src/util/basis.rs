use pyo3::prelude::*;

use crate::{fusion::state::State, model::anyon::Anyon};

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct Basis {
    state: State,
    basis: Vec<Anyon>,
}
