use crate::fusion::state::State;
use crate::model::anyon::AccessAnyon;
use pyo3::prelude::*;
use std::collections::HashMap;

use super::state::AccessState;

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
pub struct FusionPair {
    anyon_1: usize,
    anyon_2: usize,
}

impl FusionPair {
    pub fn anyon_1(&self) -> usize {
        self.anyon_1
    }
    pub fn anyon_2(&self) -> usize {
        self.anyon_2
    }
}
#[pyclass]
pub struct Fusion {
    state: State,
}

#[pymethods]
impl Fusion {
    #[new]
    fn new(state: State) -> Self {
        Fusion { state }
    }

    fn all_basis(&self) -> PyResult<Vec<FusionPair>> {
        Ok(Vec::new())
    }

    /// Builds the fusion tree's graphical representation
    /// TODO: Test this function properly. It may mostly work in its current state, but it's not
    /// guaranteed to be correct. Will need to impl with pytest and check the output.
    fn __str__(&self) -> PyResult<String> {
        // call state's get_anyons
        let anyons = self.state.get_anyons();
        let operations = self.state.get_operations();

        let active_anyons: Vec<bool> = anyons.iter().map(|_| true).collect();

        let is_join_map: HashMap<bool, String> =
            HashMap::from([(true, "─|".to_string()), (false, "|".to_string())]);

        // Anyon names
        let top_level: String = anyons
            .iter()
            .map(|a| format!("{} ", (*a).get_name()))
            .collect();

        // Anyon levels
        let level_2: String = anyons.iter().map(|_| format!("| ")).collect();

        let mut body: String = String::new();

        let prev_time: u32 = 1;
        for (time, op) in operations {
            if prev_time == time {
                body.push_str(
                    format!("{}{}", " ".repeat(op.anyon_1() * 2), is_join_map[&true]).as_str(),
                );
            } else {
                body.push_str(
                    format!(
                        "\n{}\n",
                        active_anyons
                            .iter()
                            .map(|is_active| if *is_active { " " } else { "|" })
                            .collect::<String>()
                            .to_string()
                    )
                    .as_str(),
                );
            }
        }

        Ok(format!("{}\n{}\n{}", top_level, level_2, body).to_string())
    }
}
