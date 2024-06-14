use pyo3::prelude::*;

use crate::fusion::fusion::FusionPair;

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct Basis {
    ops: Vec<(u32, Vec<FusionPair>)>,
}


#[pymethods]
impl Basis {
    #[new]
    fn new(ops: Vec<(u32, Vec<FusionPair>)>) -> Self {
        Basis { ops }
    }
}
