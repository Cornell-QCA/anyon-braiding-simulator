# Anyon Braiding Simulator
## A Brief Overview of Anyon Braiding
*Anyons* are special (quasi)particles that could allow for the realization of topological quantum computation (TQC). The topology of a system of anyons can be **resistant to perturbations** that would produce unwanted errors in other types of qubits, such that TQC is expected to be more physically robust. As anyons travel along paths through space and time, the process of *braiding* these paths (by swapping the positions of the anyons) can change the state of the anyon system. In particular, the braiding of non-Abelian anyons can apply non-commutative unitary operations to the overall state, which could result in the generation of **any sequence of quantum gate operations** with arbitrary precision, depending on the given anyon model.
## Purpose of This Project
The concepts involved in the braiding and subsequent fusion/measurement of anyons can be abstract for beginners, but there are useful diagrams that already exist which can illustrate both of these processes. This project will use these braiding and fusion diagrams to build a **graphical interface** that keeps track of user-applied changes to a system’s topology, automating the construction of anyon braid matrices and the qubit states encoded by different fusion outcomes.

The user will be able to:
- Initialize a system of anyons using a particular non-Abelian anyon model (such as the *Ising model*), thereby selecting:
  - The total number of anyons
  - The *topological charge* of each anyon
  - The relative position of each anyon
  - Optionally, the desired computational basis, which corresponds to a default fusion ordering
- Apply an arbitrary number of swaps between adjacent anyons, viewing the resulting braid that accumulates at each time step
- View the unitary matrix that corresponds to the given braid
- Access the qubit states encoded in the possible fusion outcomes that are consistent with the initialized system
- If possible, view the braid that corresponds to a given quantum gate (i.e. the reverse process of what was described above)

We hope that this project will act as a tool for beginners to learn about anyon braiding and TQC, along with related subfields like *topological error correction*. By experimenting with different input systems, the user can also gain intuition for how different anyon models affect the encoding of qubits and the resulting braid matrices.
