from anyon_braiding_simulator import Anyon, Fusion, FusionPair, IsingTopoCharge, State


def setup() -> State:
    state = State()

    return state


def test_str_1():
    state = setup()
    for i in range(6):
        state.add_anyon(Anyon(f'{i}', IsingTopoCharge.Sigma, (0, 0)))

    state.add_operation(1, FusionPair(0, 1))
    state.add_operation(1, FusionPair(2, 3))
    state.add_operation(1, FusionPair(4, 5))
    state.add_operation(2, FusionPair(2, 4))
    state.add_operation(3, FusionPair(0, 2))

    fusion = Fusion(state)
    expected = '0 1 2 3 4 5\n| | | | | |\n|─| |─| |─|\n|   |───|  \n|───|      \n|          '

    print(fusion)
    assert str(fusion) == expected
