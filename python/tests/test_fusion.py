from anyon_braiding_simulator import Anyon, Fusion, FusionPair, IsingTopoCharge, State


def setup() -> State:
    state = State()
    for i in range(7):
        state.add_anyon(Anyon(f'{i}', IsingTopoCharge.Sigma, (0, 0)))

    state.add_operation(1, FusionPair(0, 1))
    state.add_operation(1, FusionPair(2, 3))
    state.add_operation(1, FusionPair(4, 5))
    state.add_operation(2, FusionPair(2, 4))
    state.add_operation(3, FusionPair(0, 2))

    fusion = Fusion(state)

    return str(fusion)


if __name__ == '__main__':
    fusion = setup()
    print(fusion)
