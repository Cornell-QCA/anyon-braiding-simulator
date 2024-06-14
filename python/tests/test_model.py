from anyon_braiding_simulator import Anyon, IsingTopoCharge, Model


def setup():
    model = Model()
    return model


def test_apply_ising_fusion():
    model = setup()

    anyon1 = Anyon('anyon1', IsingTopoCharge.Vacuum, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Vacuum, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Vacuum

    anyon1 = Anyon('anyon1', IsingTopoCharge.Sigma, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Sigma, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Vacuum
    assert fusion_result[1].name == 'anyon1_anyon2'
    assert fusion_result[1].charge == IsingTopoCharge.Psi

    anyon1 = Anyon('anyon1', IsingTopoCharge.Psi, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Psi, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Vacuum

    anyon1 = Anyon('anyon1', IsingTopoCharge.Sigma, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Psi, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Sigma

    anyon1 = Anyon('anyon1', IsingTopoCharge.Psi, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Sigma, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Sigma

    anyon1 = Anyon('anyon1', IsingTopoCharge.Sigma, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Vacuum, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Sigma

    anyon1 = Anyon('anyon1', IsingTopoCharge.Vacuum, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Sigma, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Sigma

    anyon1 = Anyon('anyon1', IsingTopoCharge.Psi, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Vacuum, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Psi

    anyon1 = Anyon('anyon1', IsingTopoCharge.Vacuum, (0, 0))
    anyon2 = Anyon('anyon2', IsingTopoCharge.Psi, (0, 0))
    fusion_result = model.apply_fusion(anyon1, anyon2)
    assert fusion_result[0].name == 'anyon1_anyon2'
    assert fusion_result[0].charge == IsingTopoCharge.Psi
