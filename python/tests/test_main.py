# Standard Library
import os

import pytest
from unittest.mock import patch
import sh

def exec(cmds: list[str]):
    os.chdir('python/anyon_braiding_simulator')

    cmd_string = '\n'.join(cmds)

    try:
        sh.python(['main.py'], _in=cmd_string)
    except sh.ErrorReturnCode as e:
        print(e)
        assert False
    finally:
        os.chdir('../..')

class TestInit:
    @pytest.mark.main
    def test_model_ising(self):
        cmds = ['ising', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_model_fibonacci(self):
        cmds = ['fibonacci', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_one_anyon_vac(self):
        cmds = ['ising', 'anyon1 vac', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_one_anyon_sigma(self):
        cmds = ['ising', 'anyon1 sigma', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_one_anyon_psi(self):
        cmds = ['ising', 'anyon1 psi', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_one_anyon_2D(self):
        cmds = ['ising', 'anyon1 psi {1,2}', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_two_anyons(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 vac', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_three_anyons(self):
        cmds = ['ising', 'anyon1 vac', 'anyon2 sigma', 'anyon3 sigma', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_three_anyons_2D(self):
        cmds = ['ising', 'anyon1 psi {-1,-1}', 'anyon2 vac {2,-1}', 'anyon3 vac {0,0}', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_three_anyons_2D_overlapping(self):
        cmds = ['ising', 'anyon1 psi {-1,-1}', 'anyon2 vac {2,-1}', 'anyon3 vac {2,-1}', 'done', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_four_anyons(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 psi', 'anyon4 psi', 'done', 'exit']
        exec(cmds)

class TestBraidAndFuse:
    @pytest.mark.main
    def test_braid_and_print(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 sigma', 'anyon3 psi', 'done', 'braid swap 1 anyon1 anyon2', 'braid print', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_braid_and_print_2D(self):
        cmds = ['ising', 'anyon1 psi {8,-4}', 'anyon2 sigma {5,5}', 'anyon3 psi {1,-1}', 'done', 'braid swap 1 anyon1 anyon2', 'braid print', 'exit']
        exec(cmds)
    
    @pytest.mark.main
    def test_fusion(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 sigma', 'done', 'fusion 1 anyon1 anyon2', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_fusion_2D(self):
        cmds = ['ising', 'anyon1 psi {0,1}', 'anyon2 sigma {-1,500}', 'done', 'fusion 1 anyon1 anyon2', 'exit']
        exec(cmds)

class TestListAndHelp:
    @pytest.mark.main
    def test_list_one_anyon(self):
        cmds = ['ising', 'anyon1 psi', 'done', 'list', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_list_three_anyons(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 vac', 'done', 'list', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_list_three_anyons_2D(self):
        cmds = ['ising', 'anyon1 psi {9,17}', 'anyon2 psi {4,-106}', 'anyon3 vac {-1,4}', 'done', 'list', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_help_command(self):
        cmds = ['ising', 'anyon1 psi', 'done', 'help', 'exit']
        exec(cmds)

class TestInvalidCommands:
    @pytest.mark.main
    def test_model_invalid(self):
        cmds = ['derp', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_anyon_invalid_charge(self):
        cmds = ['ising', 'anyon1 derp', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_invalid_command_post_init(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 psi', 'done', 'derp', 'exit']
        exec(cmds)
    
    @pytest.mark.main
    def test_invalid_braid_syntax(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 psi', 'done', 'braid swap derp derp', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_invalid_fusion_syntax(self):
        cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 psi', 'done', 'fusion derp derp', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_model_post_init(self):
        cmds = ['ising', 'anyon1 psi', 'done', 'model fibonacci', 'exit']
        exec(cmds)

    @pytest.mark.main
    def test_anyon_post_init(self):
        cmds = ['ising', 'anyon1 psi', 'done', 'anyon anyon2 psi', 'exit']
        exec(cmds)


# @pytest.mark.main
# def test_shell():
#     with patch('subprocess.run') as mock_run:
#         shell = SimulatorShell()
#         shell.do_shell('echo Let\'s go, Brandon!')
#         mock_run.assert_called_once_with('echo Hello, World!', shell=True)
