use numpy::ndarray::Array1;
use numpy::{Complex64, PyArray1, PyReadonlyArray1, ToPyArray};
use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug)]
/// State Vector for the system
pub struct StateVec {
    vec: Array1<Complex64>,
    #[pyo3(get)]
    init_size: usize,
}

/// Internal Methods
impl StateVec {
    /// Returns a clone of the state vector
    pub fn get_vec(&self) -> Array1<Complex64> {
        self.vec.clone()
    }
    /// Modifies the norm of the state vector to 1
    pub fn normalize(&mut self) {
        let norm = self.vec.iter().map(|x| x.norm_sqr()).sum::<f64>().sqrt();
        for i in 0..self.vec.len() {
            self.vec[i] /= Complex64::new(norm, 0.0);
        }
    }
}


/// Python Methods
#[pymethods]
impl StateVec {
    #[new]
    /// Creates a new state vector. If no vector is provided, it will be
    /// initialized to 0. Additionally, the vector will be normalized.
    pub fn new(qubit_num: usize, vec: Option<PyReadonlyArray1<Complex64>>) -> Self {
        let init_size = 2 << qubit_num;
        let vec = match vec {
            Some(vec) => vec.as_array().to_owned(),
            None => Array1::zeros(init_size),
        };

        // normalize the vector
        let mut state_vec = StateVec { vec, init_size };
        state_vec.normalize();
        state_vec
    }

    #[getter]
    fn vec(&self, py: Python<'_>) -> PyResult<Py<PyArray1<Complex64>>> {
        Ok(self.vec.to_pyarray_bound(py).to_owned().into())
    }

    #[setter]
    pub fn set_size(&mut self, qubit_num: usize) {
        self.init_size = 2 << qubit_num;
        self.vec = Array1::zeros(self.init_size);
    }

    pub fn __str__(&self) -> PyResult<String> {
        let mut output: String = "[\n".to_string();
        for val in self.vec.iter() {
            output.push_str(&format!("\t{:?} + {:?}i\n", val.re, val.im));
        }
        output.push_str("]");
        Ok(output)
    }
}
