use pyo3::prelude::*;
mod fusion;
mod model;
mod util;

/// A Python module implemented in Rust.
#[pymodule]
fn anyon_braiding_simulator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<model::anyon::Anyon>()?;
    m.add_class::<model::anyon::IsingTopoCharge>()?;

    m.add_class::<model::model::Model>()?;
    m.add_class::<model::model::AnyonModel>()?;

    m.add_class::<fusion::fusion::Fusion>()?;
    m.add_class::<fusion::fusion::FusionPair>()?;

    m.add_class::<fusion::state::State>()?;
    Ok(())
}
