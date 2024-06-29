# Standard Library
import os

import pytest
import sh


def exec(model, cmds: list[str]):
    os.chdir('python/anyon_braiding_simulator')

    # Insert the model at the beginning of cmds, & join them into a single string
    cmds.insert(0, model)
    cmd_string = '\n'.join(cmds)

    try:
        sh.python(['main.py'], _in=cmd_string)
    except sh.ErrorReturnCode as e:
        print(e)
        assert False
    finally:
        os.chdir('../..')


class TestInit:
    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_model_ising(self, model):
        cmds = ['exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_three_anyons_ising(self):
        model = 'ising'
        cmds = ['anyon1 vac', 'anyon2 sigma', 'anyon3 sigma', 'done', 'exit']
        exec(model, cmds)
    
    @pytest.mark.main
    def test_three_anyons_fib(self):
        model = 'fibonacci'
        cmds = ['anyon1 vac', 'anyon2 tau', 'anyon3 tau', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_three_anyons_2D(self, model):
        cmds = ['anyon1 vac {-1,-1}', 'anyon2 vac {2,-1}', 'anyon3 vac {0,0}', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_three_anyons_2D_overlapping(self, model):
        cmds = ['anyon1 vac {-1,-1}', 'anyon2 vac {2,-1}', 'anyon3 vac {2,-1}', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_four_anyons(self, model):
        cmds = ['anyon1 vac', 'anyon2 vac', 'anyon3 vac', 'anyon4 vac', 'done', 'exit']
        exec(model, cmds)

class TestBraidAndFuse:
    @pytest.mark.main
    def test_braid_and_print_ising(self):
        model = 'ising'
        cmds = ['anyon1 psi', 'anyon2 sigma', 'anyon3 psi', 'done', 'braid swap anyon1-anyon2', 'braid print', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_braid_and_print_fib(self):
        model = 'fibonacci'
        cmds = ['anyon1 tau', 'anyon2 tau', 'anyon3 tau', 'done', 'braid swap anyon1-anyon2', 'braid print', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_braid_and_print_2D_ising(self):
        model = 'ising'
        cmds = ['anyon1 psi {8,-4}', 'anyon2 sigma {5,5}', 'anyon3 psi {1,-1}', 'done', 'braid swap anyon1-anyon2', 'braid print', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_braid_and_print_2D_fib(self):
        model = 'fibonacci'
        cmds = ['anyon1 tau {8,-4}', 'anyon2 tau {5,5}', 'anyon3 tau {1,-1}', 'done', 'braid swap anyon1-anyon2', 'braid print', 'exit']
        exec(model, cmds)

class TestListAndHelp:
    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_list_three_anyons(self, model):
        cmds = ['anyon1 vac', 'anyon2 vac', 'anyon3 vac', 'done', 'list', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_list_three_anyons_2D(self, model):
        cmds = ['anyon1 vac {9,17}', 'anyon2 vac {4,-106}', 'anyon3 vac {-1,4}', 'done', 'list', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_help_command(self, model):
        cmds = ['anyon1 vac', 'done', 'help', 'exit']
        exec(model, cmds)

class TestInvalidCommands:
    @pytest.mark.main
    def test_model_invalid(self):
        model = 'derp'
        cmds = ['exit']
        exec(model, cmds)
    
    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_one_anyon_vac(self, model):
        cmds = ['anyon1 vac', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_one_anyon_sigma(self):
        model = 'ising'
        cmds = ['anyon1 sigma', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_one_anyon_psi(self):
        model = 'ising'
        cmds = ['anyon1 psi', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_one_anyon_tau(self):
        model = 'fibonacci'
        cmds = ['anyon1 tau', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_one_anyon_2D_ising(self):
        model = 'ising'
        cmds = ['anyon1 psi {1,2}', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_one_anyon_2D_fib(self):
        model = 'fibonacci'
        cmds = ['anyon1 tau {1,2}', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_two_anyons_ising(self):
        model = 'ising'
        cmds = ['anyon1 psi', 'anyon2 vac', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.main
    def test_two_anyons_fib(self):
        model = 'fibonacci'
        cmds = ['anyon1 tau', 'anyon2 vac', 'done', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_anyon_invalid_charge(self, model):
        cmds = ['anyon1 derp', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_anyon_invalid_position1(self, model):
        cmds = ['anyon1 vac {3, 4, 5}', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_anyon_invalid_position2(self, model):
        cmds = ['anyon1 vac {5,}', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_anyon_invalid_position3(self, model):
        cmds = ['anyon1 vac [4,5]', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_anyon_invalid_position4(self, model):
        cmds = ['anyon1 vac {3; 5}', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_invalid_command_post_init(self, model):
        cmds = ['anyon1 vac', 'anyon2 vac', 'anyon3 vac', 'done', 'derp', 'exit']
        exec(model, cmds)
    
    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_invalid_braid_syntax(self, model):
        cmds = ['anyon1 vac', 'anyon2 vac', 'anyon3 vac', 'done', 'braid swap derp-derp', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_list_one_anyon(self, model):
        cmds = ['anyon1 vac', 'done', 'list', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_model_post_init(self, model):
        cmds = ['anyon1 vac', 'done', 'model fibonacci', 'exit']
        exec(model, cmds)

    @pytest.mark.parametrize('model', ['ising', 'fibonacci'])
    @pytest.mark.main
    def test_anyon_post_init(self, model):
        cmds = ['anyon1 vac', 'done', 'anyon anyon2 vac', 'exit']
        exec(model, cmds)
