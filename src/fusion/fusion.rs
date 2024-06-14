use crate::fusion::state::AccessState;
use crate::fusion::state::State;
use crate::model::anyon::AccessAnyon;
use crate::util::basis::Basis;
use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct FusionPair {
    #[pyo3(get)]
    anyon_1: usize,
    #[pyo3(get)]
    anyon_2: usize,
}

pub trait AccessFusionPair {
    fn anyon_1(&self) -> usize;
    fn anyon_2(&self) -> usize;
}

impl AccessFusionPair for FusionPair {
    fn anyon_1(&self) -> usize {
        self.anyon_1
    }
    fn anyon_2(&self) -> usize {
        self.anyon_2
    }
}

#[pymethods]
impl FusionPair {
    #[new]
    fn new(anyon_1: usize, anyon_2: usize) -> Self {
        FusionPair { anyon_1, anyon_2 }
    }
}

#[pyclass]
pub struct Fusion {
    state: State,
    ops: Vec<Vec<(usize, usize)>>,
}

#[pymethods]
impl Fusion {
    #[new]
    fn new(state: State) -> Self {
        let operations = state.operations();

        let mut ops: Vec<Vec<(usize, usize)>> = Vec::new();

        let mut prev_time = 0;
        for (time, op) in operations {
            if prev_time == time {
                ops[time as usize - 1].push((op.anyon_1(), op.anyon_2()));
            } else {
                ops.push(vec![(op.anyon_1(), op.anyon_2())]);
                prev_time = time;
            }
        }

        Fusion { state, ops }
    }

    fn all_basis(&self) -> PyResult<Vec<Basis>> {
        unimplemented!()
    }

    fn verify_basis(&self, basis: &Basis) -> PyResult<bool> {
        // Naive, there's better ways to improve avg performance. Will deal with
        // it once we have the basis implementation
        Ok(self.all_basis().unwrap().contains(basis))
    }

    /// Builds the fusion tree's graphical representation
    fn __str__(&self) -> PyResult<String> {
        // call state's get_anyons
        let anyons = self.state.anyons();

        let mut active_anyons: Vec<bool> = anyons.iter().map(|_| true).collect();

        // Anyon names
        let top_level: String = anyons.iter().map(|a| format!("{} ", (*a).name())).collect();

        // Anyon levels
        let level_2: String = anyons.iter().map(|_| format!("| ")).collect();

        let mut body: String = String::new();

        for level in self.ops.iter() {
            // even indices are for anyons, odd indices are for operations (i.e. joining or no action)
            let mut level_vec = vec![" "; 2 * anyons.len()];
            // set active anyons with a pipe
            level_vec.iter_mut().enumerate().for_each(|(i, v)| {
                if i % 2 == 0 && active_anyons[i / 2] {
                    *v = "|";
                }
            });

            for (anyon_1, anyon_2) in level.iter() {
                let start =  2 * (*anyon_1) + 1;
                let end = 2 * (*anyon_2) ;
                for i in start..end {
                    level_vec[i] = "─";
                }
                active_anyons[*anyon_2] = false;
            }

            body.push_str(&format!("{}\n", level_vec.join("")));
        }

        let last_time = format!(
            "{}",
            active_anyons
                .iter()
                .map(|is_active| if *is_active { "| " } else { "  " })
                .collect::<String>()
                .to_string()
        );

        Ok(format!("{}\n{}\n{}{}", top_level, level_2, body, last_time).to_string())
    }
}
