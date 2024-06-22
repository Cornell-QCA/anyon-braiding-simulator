use pyo3::prelude::*;

use crate::fusion::fusion::FusionPair;

#[pyclass]
#[derive(Clone, Debug, PartialEq)]
/// The basis is represented as a vector of tuples (time, FusionPair). In TQC,
/// the basis is a sequence of fusion operations that occur in the fusion tree,
/// and a different fusion ordering is a different basis.
pub struct Basis {
    ops: Vec<(u32, FusionPair)>,
}

#[pymethods]
impl Basis {
    #[new]
    fn new(ops: Vec<(u32, FusionPair)>) -> Self {
        Basis { ops }
    }

    /// Verifies the basis
    /// Preconditions: sorted by time
    pub fn verify_basis(&self, anyons: usize) -> bool {
        if self.ops.len() != anyons - 1 {
            return false;
        }

        let mut fusible_anyons = vec![true; anyons];
        let mut unused_anyons = vec![true; anyons];

        let mut current_time: u32 = 0;

        for (t, op) in &self.ops {
            if *t != current_time {
                unused_anyons = vec![true; anyons];
                current_time = *t;
            }

            // Anyons in fuision pair is not in range [0,anyons)
            if !(op.anyon_1() < op.anyon_2() && op.anyon_2() < anyons) {
                return false;
            }

            // Anyons have been fusioned away at a previous time
            if !fusible_anyons[op.anyon_1()] || !fusible_anyons[op.anyon_2()] {
                return false;
            }

            // Anyons have already been fusioned at the current time
            if !unused_anyons[op.anyon_1()] || !unused_anyons[op.anyon_2()] {
                return false;
            }

            // Checks for adjacency of anyon_1 and anyon_2
            for anyon in op.anyon_1() + 1..op.anyon_2() - 1 {
                if fusible_anyons[anyon] && unused_anyons[anyon] {
                    return false;
                }
            }

            fusible_anyons[op.anyon_2()] = false;
            unused_anyons[op.anyon_1()] = false;
        }

        true
    }
}
