from anyon_braiding_simulator import Basis, FusionPair


def setup():
    pass


# Test basic input sanitizations
def test_basis():
    anyons = 10
    operations = []
    for t in range(1, 10):
        operations.append((t, FusionPair(0, t)))

    assert Basis(operations).verify_basis(anyons)

    operations = []

    assert not Basis(operations).verify_basis(anyons)

    operations = []
    for t in range(1, 10):
        operations.append((t, FusionPair(t, 0)))

    assert not Basis(operations).verify_basis(anyons)

    operations = []

    for t in range(1, 10):
        operations.append((1, FusionPair(0, t)))

    assert not Basis(operations).verify_basis(anyons)
