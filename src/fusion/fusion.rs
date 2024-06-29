use std::collections::HashMap;

use crate::fusion::state::State;
use crate::model::anyon::FibonacciTopoCharge;
use crate::model::anyon::IsingTopoCharge;
use crate::model::anyon::TopoCharge;
use crate::model::model::AnyonModel;
use crate::util::basis::Basis;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug, PartialEq, Hash, Eq, Ord, PartialOrd)]
/// Represents a pair of anyons indices that are fused. The indices are derived
/// from the relative ordering in the list of anyons stored in State.
/// FusionPair is used to represent the fusion events along the fusion tree.
///
/// When two anyons are fused, the resulting anyon carries the lower index. i.e.
/// the anyon resulting from the fusion (1,2) is later referenced as 1
pub struct FusionPair {
    #[pyo3(get)]
    anyon_1: usize,
    #[pyo3(get)]
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
/// Stores the state of the system and all fusion operations that occur in the
/// fusion tree. The vector is 2D, where the outer vector represents the time
/// step and the inner vector represents the fusion operations that occur at
/// that time step.
pub struct Fusion {
    state: State,
    ops: Vec<Vec<FusionPair>>,
}

/// Internal Methods
impl Fusion {
    /// Converts from IsingTopoCharge to internal format
    /// Format is [psi, vacuum, sigma]  (so we can use the index as the encode)
    pub fn ising_canonical_topo_charge(&self, charge: IsingTopoCharge) -> Vec<u64> {
        match charge {
            IsingTopoCharge::Psi => vec![1, 0, 0],
            IsingTopoCharge::Vacuum => vec![0, 1, 0],
            IsingTopoCharge::Sigma => vec![0, 0, 1],
        }
    }

    /// Converts from FibonacciTopoCharge to internal format
    /// Format is [tau, vacuum]  (so we can use the index as the encode)
    pub fn fibonacci_canonical_topo_charge(&self, charge: FibonacciTopoCharge) -> Vec<u64> {
        match charge {
            FibonacciTopoCharge::Tau => vec![1, 0],
            FibonacciTopoCharge::Vacuum => vec![0, 1],
        }
    }

    /// Creates a qubit encoding for the Ising model from the fusion tree. The encoding is a list of
    /// FusionPairs that represent the anyons that are fused to create the qubit
    /// encoding.
    pub fn ising_qubit_enc(&self) -> Vec<FusionPair> {
        let mut tcs: Vec<Vec<u64>> = self
            .state
            .anyons()
            .iter()
            .map(|a| self.ising_canonical_topo_charge(a.charge().get_ising()))
            .collect();
        let mut fusion_pair_tc: HashMap<FusionPair, Vec<u64>> = HashMap::new();

        let mut final_tc: Vec<u64> = vec![0, 0, 0];

        for (i, op) in self.ops.iter().enumerate() {
            for (j, fusion_pair) in op.iter().enumerate() {
                let tc = self.ising_apply_fusion(
                    tcs[fusion_pair.anyon_1()].clone(),
                    tcs[fusion_pair.anyon_2()].clone(),
                );
                if i == self.ops.len() - 1 && j == op.len() - 1 {
                    final_tc = tc;
                    break;
                }
                fusion_pair_tc.insert(fusion_pair.clone(), tc.clone());
                tcs[fusion_pair.anyon_1()] = tc;
            }
        }

        if final_tc[IsingTopoCharge::Sigma.value()] == 0
            && ((final_tc[IsingTopoCharge::Psi.value()] == 1
                && final_tc[IsingTopoCharge::Vacuum.value()] == 0)
                || (final_tc[IsingTopoCharge::Psi.value()] == 1
                    && final_tc[IsingTopoCharge::Vacuum.value()] == 0))
        {
            return Vec::new();
        }

        let mut encoding_fusions: Vec<FusionPair> = fusion_pair_tc
            .into_iter()
            .filter(|(_, tc)| tc[IsingTopoCharge::Sigma.value()] == 0)
            .map(|(fusion_pair, _)| fusion_pair)
            .collect();
        encoding_fusions.sort();
        encoding_fusions.pop().unwrap();
        encoding_fusions
    }

    /// Creates a qubit encoding for the Fibonacci model from the fusion tree. The encoding is a list of
    /// FusionPairs that represent the anyons that are fused to create the qubit
    /// encoding.
    pub fn fibonacci_qubit_enc(&self) -> Vec<FusionPair> {
        unimplemented!()
    }

    /// Applies the fusion rules to two anyons and returns the resulting anyon(s).
    pub fn ising_apply_fusion(&self, anyon_1: Vec<u64>, anyon_2: Vec<u64>) -> Vec<u64> {
        assert!(anyon_1.len() == 3 && anyon_2.len() == 3);

        let add = |a: [u64; 3], b: [u64; 3]| -> [u64; 3] { std::array::from_fn(|i| a[i] + b[i]) };
        let arr_scale = |a: [u64; 3], b: u64| -> [u64; 3] { std::array::from_fn(|i| a[i] * b) };

        let mut output = [0 as u64; 3];

        // ising fusion rules
        // symmetric matrix which is built from fusion rules of (psi, 1, sigma) ^ (psi, 1, sigma)
        let fusion_rules_mtx: [[[u64; 3]; 3]; 3] = [
            [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
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

        Vec::from(output)
    }
    /// Applies the fusion rules to two anyones and returns the resulting anyon(s).
    fn fibonacci_apply_fusion(&self, anyon_1: Vec<u64>, anyon_2: Vec<u64>) -> Vec<u64> {
        assert!(anyon_1.len() == 2 && anyon_2.len() == 2);

        let add = |a: [u64; 2], b: [u64; 2]| -> [u64; 2] { std::array::from_fn(|i| a[i] + b[i]) };
        let arr_scale = |a: [u64; 2], b: u64| -> [u64; 2] { std::array::from_fn(|i| a[i] * b) };

        let mut output = [0 as u64; 2];

        // ising fusion rules
        // symmetric matrix which is built from fusion rules of (tau, 1) ^ (tau, 1)
        let fusion_rules_mtx: [[[u64; 2]; 2]; 2] = [[[1, 1], [1, 0]], [[1, 0], [0, 1]]];

        // build the outer product of the two tc vectors
        let mut tc_mtx = [[0; 2]; 2];
        for i in 0..2 {
            for j in 0..2 {
                tc_mtx[i][j] = anyon_1[i] * anyon_2[j];
            }
        }

        // mtx multiply fusion rules with tc_mtx
        for i in 0..2 {
            for j in 0..2 {
                output = add(output, arr_scale(fusion_rules_mtx[i][j], tc_mtx[i][j]));
            }
        }

        Vec::from(output)
    }

    /// Checks if an overall fusion result is possible given the state's
    /// configuration and an initial topo charge under the Ising model
    ///
    /// Precondition: Non empty list of anyons
    pub fn ising_verify_fusion_result(&self, init_charge: IsingTopoCharge) -> bool {
        let overall_fusion_result: Vec<u64> = self
            .state
            .anyons()
            .iter()
            .map(|a| self.ising_canonical_topo_charge(a.charge().get_ising()))
            .reduce(|acc, tc| self.ising_apply_fusion(acc, tc))
            .unwrap();

        // if an element > 0 that means it was our initial charge, so we need to
        // check if our final fusion result also has that element > 0
        overall_fusion_result
            .iter()
            .zip(self.ising_canonical_topo_charge(init_charge).iter())
            .all(|(a, b)| *b <= 0 || *a > 0)
    }

    /// Checks if an overall fusion result is possible given the state's
    /// configuration and an initial topo charge under the Fibonacci model
    ///
    /// Precondition: Non empty list of anyons
    pub fn fibonacci_verify_fusion_result(&self, init_charge: FibonacciTopoCharge) -> bool {
        let overall_fusion_result: Vec<u64> = self
            .state
            .anyons()
            .iter()
            .map(|a| self.fibonacci_canonical_topo_charge(a.charge().get_fibonacci()))
            .reduce(|acc, tc| self.fibonacci_apply_fusion(acc, tc))
            .unwrap();

        // if an element > 0 that means it was our initial charge, so we need to
        // check if our final fusion result also has that element > 0
        overall_fusion_result
            .iter()
            .zip(self.fibonacci_canonical_topo_charge(init_charge).iter())
            .all(|(a, b)| *b <= 0 || *a > 0)
    }

    ///
    /// Returns number of sigmas that can be in the initial topological charges of anyons to exactly a certain number of qubits for the Ising model
    ///
    pub fn ising_possible_sigmas(&self, qubits: u32) -> Vec<u32> {
        vec![2 * qubits + 1, 2 * qubits + 2]
    }
    ///
    /// Returns number of taus that can be in the initial topological charges of anyons to exactly a certain number of qubits for the Fibonacci model
    ///
    /// Precondition: Requires qubits <=30
    pub fn fibonacci_possible_taus(&self, qubits: u32) -> Vec<u32> {
        if qubits == 0 {
            return vec![0, 1, 2, 3];
        }

        let mut possible_taus = Vec::new();

        let mut n = 1;

        // We have that the fibonacci recurrence gives us that tau^n = a + b * tau
        let mut a = 0;
        let mut b = 1;

        // Checks that b < 2^(qubits+1) meaning as otherwise fusing to tau would result in too many qubits
        while b < 1 << (qubits + 1) {
            // If b >= 2^qubits we have that this will give exactly 'qubits' qubits
            if (1 << (qubits)) <= b {
                possible_taus.push(n);
            }

            b = a + b;
            a = b - a;

            n += 1;
        }
        // Accounts for the case that we can also fuse to vaccuum
        possible_taus.push(n);
        possible_taus
    }
}

/// Python Facing Methods
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

    fn qubit_enc(&self) -> PyResult<Vec<FusionPair>> {
        match self.state.anyon_model() {
            AnyonModel::Ising => Ok(self.ising_qubit_enc()),
            AnyonModel::Fibonacci => Ok(self.fibonacci_qubit_enc()),
            _ => Err(PyValueError::new_err("This model is not supported yet")),
        }
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

    fn apply_fusion(&self, anyon_1: Vec<u64>, anyon_2: Vec<u64>) -> PyResult<Vec<u64>> {
        match self.state.anyon_model() {
            AnyonModel::Ising => Ok(self.ising_apply_fusion(anyon_1, anyon_2)),
            AnyonModel::Fibonacci => Ok(self.fibonacci_apply_fusion(anyon_1, anyon_2)),
            _ => Err(PyValueError::new_err("This model is not supported yet")),
        }
    }

    fn verify_fusion_result(&self, init_charge: TopoCharge) -> bool {
        match self.state.anyon_model() {
            AnyonModel::Ising => self.ising_verify_fusion_result(init_charge.get_ising()),
            AnyonModel::Fibonacci => {
                self.fibonacci_verify_fusion_result(init_charge.get_fibonacci())
            }
            _ => false,
        }
    }
    fn minimum_possible_anyons(&self, qubits: u32) -> PyResult<Vec<u32>> {
        match self.state.anyon_model() {
            AnyonModel::Ising => Ok(self.ising_possible_sigmas(qubits)),
            AnyonModel::Fibonacci => Ok(self.fibonacci_possible_taus(qubits)),
            _ => Err(PyValueError::new_err("This model is not supported yet")),
        }
    }
}
