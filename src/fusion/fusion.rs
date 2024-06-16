use std::collections::HashMap;

use crate::fusion::state::AccessState;
use crate::fusion::state::State;
use crate::model::anyon::AccessAnyon;
use crate::model::anyon::IsingTopoCharge;
use crate::util::basis::Basis;
use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug, PartialEq, Hash, Eq, Ord, PartialOrd)]
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

    fn __str__(&self) -> PyResult<String> {
        Ok(format!("({} {})", self.anyon_1, self.anyon_2))
    }
}

#[pyclass]
pub struct Fusion {
    state: State,
    ops: Vec<Vec<FusionPair>>,
}

#[pymethods]
impl Fusion {
    #[new]
    fn new(state: State) -> Self {
        let operations = state.operations();

        let mut ops: Vec<Vec<FusionPair>> = Vec::new();

        let mut prev_time = 0;
        for (time, op) in operations {
            if prev_time == time {
                ops[time as usize - 1].push(op);
            } else {
                ops.push(vec![op]);
                prev_time = time;
            }
        }

        Fusion { state, ops }
    }

    /// Verifies the basis
    fn verify_basis(&self, basis: &Basis) -> PyResult<bool> {
        Ok(basis.verify_basis(self.state.anyons().len()))
    }

    /// Assumes model is Ising
    /// TODO: THIS IS NON DETERMINISTIC WTF
    fn qubit_enc(&self) -> PyResult<Vec<FusionPair>> {
        let enum_to_canonical = |charge: IsingTopoCharge| -> [u64; 3] {
            match charge {
                IsingTopoCharge::Psi => [1, 0, 0],
                IsingTopoCharge::Vacuum => [0, 1, 0],
                IsingTopoCharge::Sigma => [0, 0, 1],
            }
        };
        let mut tcs: Vec<[u64; 3]> = self
            .state
            .anyons()
            .iter()
            .map(|a| enum_to_canonical(a.charge()))
            .collect();
        let mut fusion_pair_tc: HashMap<FusionPair, [u64; 3]> = HashMap::new();

        let mut final_tc: [u64; 3] = [0, 0, 0];

        for (i, op) in self.ops.iter().enumerate() {
            for (j, fusion_pair) in op.iter().enumerate() {
                let tc =
                    self.apply_fusion(tcs[fusion_pair.anyon_1()], tcs[fusion_pair.anyon_2()])?;
                if i == self.ops.len() - 1 && j == op.len() - 1 {
                    final_tc = tc;
                    break;
                }
                fusion_pair_tc.insert(fusion_pair.clone(), tc);
                tcs[fusion_pair.anyon_1()] = tc;
            }
        }

        if final_tc[IsingTopoCharge::Sigma.value()] == 0
            && ((final_tc[IsingTopoCharge::Psi.value()] == 1
                && final_tc[IsingTopoCharge::Vacuum.value()] == 0)
                || (final_tc[IsingTopoCharge::Psi.value()] == 1
                    && final_tc[IsingTopoCharge::Vacuum.value()] == 0))
        {
            return Ok(Vec::new());
        }

        let mut encoding_fusions: Vec<FusionPair> = fusion_pair_tc
            .into_iter()
            .filter(|(_, tc)| tc[IsingTopoCharge::Sigma.value()] == 0)
            .map(|(fusion_pair, _)| fusion_pair)
            .collect();
        encoding_fusions.sort();
        encoding_fusions.pop().unwrap();
        Ok(encoding_fusions)
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

            //
            // here rishi :3
            //
            for fusion_pair in level.iter() {
                let start = 2 * (fusion_pair.anyon_1()) + 1;
                let end = 2 * (fusion_pair.anyon_2());
                for i in start..end {
                    level_vec[i] = "─";
                }
                active_anyons[fusion_pair.anyon_2()] = false;
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

    /// Fuses anyons according to their fusion rules
    /// TODO: Generalize this to all models (has to be known size)
    /// Format is [psi, vacuum, sigma]  (so we can use the index as the encode)
    pub fn apply_fusion(&self, anyon_1: [u64; 3], anyon_2: [u64; 3]) -> PyResult<[u64; 3]> {
        let add = |a: [u64; 3], b: [u64; 3]| -> [u64; 3] { std::array::from_fn(|i| a[i] + b[i]) };
        let arr_scale = |a: [u64; 3], b: u64| -> [u64; 3] { std::array::from_fn(|i| a[i] * b) };

        let mut output = [0 as u64; 3];

        // ising fusion rules
        // symmetric matrix which is built from fusion rules of (psi, 1, sigma) ^ (psi, 1, sigma)
        let fusion_rules_mtx = [
            [[0 as u64, 1, 0], [1, 0, 0], [0, 0, 1]],
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 0, 1], [0, 0, 1], [1, 1, 0]],
        ];

        // build the outer product of the two tc vectors
        let mut tc_mtx = [[0; 3]; 3];
        for i in 0..tc_mtx.len() {
            for j in 0..tc_mtx[i].len() {
                tc_mtx[i][j] = anyon_1[i] * anyon_2[j];
            }
        }

        // mtx multiply fusion rules with tc_mtx
        for i in 0..3 {
            for j in 0..3 {
                output = add(output, arr_scale(fusion_rules_mtx[i][j], tc_mtx[i][j]));
            }
        }

        return Ok(output);
    }
}
