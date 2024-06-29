import pytest
from anyon_braiding_simulator import Anyon, AnyonModel, Fusion, FusionPair, IsingTopoCharge, FibonacciTopoCharge, State, TopoCharge


@pytest.fixture
def ising_state() -> State:
    state = State()
    for i in range(6):
        state.add_anyon(Anyon(f'{i}', TopoCharge.from_ising(IsingTopoCharge.Sigma), (0, 0)))
    return state

@pytest.fixture
def fibo_state() -> State:
    state = State()
    state.set_anyon_model(AnyonModel.Fibonacci)
    for i in range(6):
        state.add_anyon(Anyon(f'{i}', TopoCharge.from_fibonacci(FibonacciTopoCharge.Tau), (0,0)))
    return state

@pytest.mark.fusion
def test_str_1(ising_state):
    ising_state.add_operation(1, FusionPair(0, 1))
    ising_state.add_operation(1, FusionPair(2, 3))
    ising_state.add_operation(1, FusionPair(4, 5))
    ising_state.add_operation(2, FusionPair(2, 4))
    ising_state.add_operation(3, FusionPair(0, 2))

    fusion = Fusion(ising_state)
    expected = '0 1 2 3 4 5 \n| | | | | | \n|─| |─| |─| \n|   |───|   \n|───|       \n|           '

    assert str(fusion) == expected


@pytest.mark.fusion
def test_apply_ising_fusion(ising_state):
    fusion = Fusion(ising_state)

    psi = [1, 0, 0]
    vacuum = [0, 1, 0]
    sigma = [0, 0, 1]

    assert fusion.apply_fusion(psi, psi) == vacuum
    assert fusion.apply_fusion(vacuum, vacuum) == vacuum
    assert fusion.apply_fusion(sigma, sigma) == [psi[i] + vacuum[i] for i in range(3)]

    psi_sigma = [1, 0, 1]
    assert fusion.apply_fusion(psi_sigma, psi_sigma) == [1, 2, 2]
    assert not fusion.apply_fusion(psi_sigma, psi_sigma) == [2, 1, 2]  # get owned rishi

@pytest.mark.fusion
def test_apply_fibo_fusion(fibo_state):
    fusion = Fusion(fibo_state)

    tau = [1,0]
    vac = [0,1]

    assert fusion.apply_fusion(tau, tau) == [1,1]
    assert fusion.apply_fusion(vac,vac) == vac
    assert fusion.apply_fusion(tau, vac) == tau

    tau_vac = [1,1]

    assert fusion.apply_fusion(tau_vac,  tau_vac) == [3,2]

@pytest.mark.fusion
def test_ising_qubit_enc(ising_state):
    ising_state.add_operation(1, FusionPair(0, 1))
    ising_state.add_operation(1, FusionPair(2, 3))
    ising_state.add_operation(1, FusionPair(4, 5))
    ising_state.add_operation(2, FusionPair(2, 4))
    ising_state.add_operation(3, FusionPair(0, 2))

    fusion = Fusion(ising_state)
    correct = [FusionPair(0, 1), FusionPair(2, 4), FusionPair(2, 3)]

    assert set(map(str, fusion.qubit_enc())) == set(map(str, correct))

@pytest.mark.fusion
def test_fibo_qubit_enc(fibo_state):
    fibo_state.add_operation(1, FusionPair(0, 1))
    fibo_state.add_operation(1, FusionPair(2, 3))
    fibo_state.add_operation(1, FusionPair(4, 5))
    fibo_state.add_operation(2, FusionPair(2, 4))
    fibo_state.add_operation(3, FusionPair(0, 2))

    fusion =  Fusion(fibo_state)

    print(fusion.qubit_enc())
    pass



@pytest.mark.fusion
def test_ising_verify_fusion_result(ising_state):
    fusion = Fusion(ising_state)
    assert not fusion.verify_fusion_result(TopoCharge.from_ising(IsingTopoCharge.Sigma))
    assert fusion.verify_fusion_result(TopoCharge.from_ising(IsingTopoCharge.Vacuum))
    assert fusion.verify_fusion_result(TopoCharge.from_ising(IsingTopoCharge.Psi))

    ising_state.add_anyon(Anyon('7', TopoCharge.from_ising(IsingTopoCharge.Sigma), (0, 0)))
    fusion = Fusion(ising_state)
    assert not fusion.verify_fusion_result(TopoCharge.from_ising(IsingTopoCharge.Vacuum))
    assert not fusion.verify_fusion_result(TopoCharge.from_ising(IsingTopoCharge.Psi))
    assert fusion.verify_fusion_result(TopoCharge.from_ising(IsingTopoCharge.Sigma))

@pytest.mark.fusion
def test_fibo_verify_fusion_result(fibo_state):
    fusion = Fusion(fibo_state)

    assert fusion.verify_fusion_result(TopoCharge.from_fibonacci(FibonacciTopoCharge.Tau))
    assert fusion.verify_fusion_result(TopoCharge.from_fibonacci(FibonacciTopoCharge.Vacuum))
    
    state = State()
    state.set_anyon_model(AnyonModel.Fibonacci)
    for i in range(6):
        state.add_anyon(Anyon(f'{i}', TopoCharge.from_fibonacci(FibonacciTopoCharge.Vacuum), (0,0)))
    fusion = Fusion(state)

    assert not fusion.verify_fusion_result(TopoCharge.from_fibonacci(FibonacciTopoCharge.Tau))
    assert fusion.verify_fusion_result(TopoCharge.from_fibonacci(FibonacciTopoCharge.Vacuum))


    

@pytest.mark.fusion
def test_ising_minimum_possible_anyons(ising_state):

    fusion = Fusion(ising_state)

    assert (fusion.minimum_possible_anyons(10) == [21,22])
    assert (fusion.minimum_possible_anyons(5) == [11,12])

@pytest.mark.fusion
def test_fibo_minimum_possible_anyons(ising_state):
    ising_state.set_anyon_model(AnyonModel.Fibonacci)
    fusion = Fusion(ising_state)

    assert(fusion.minimum_possible_anyons(10) == [17,18])
    assert(fusion.minimum_possible_anyons(0) == [0,1,2,3])
