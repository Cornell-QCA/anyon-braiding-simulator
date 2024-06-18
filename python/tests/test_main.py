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


@pytest.mark.main
def test_model_ising():
    cmds = ['ising', 'exit']
    exec(cmds)

@pytest.mark.main
def test_model_fibonacci():
    cmds = ['fibonacci', 'exit']
    exec(cmds)

@pytest.mark.main
def test_model_invalid():
    cmds = ['derp', 'exit']
    exec(cmds)

@pytest.mark.main
def test_model_post_init():
    cmds = ['ising', 'anyon1 psi', 'done', 'model fibonacci', 'exit']
    exec(cmds)

@pytest.mark.main
def test_anyon_post_init():
    cmds = ['ising', 'anyon1 psi', 'done', 'anyon anyon2 psi', 'exit']
    exec(cmds)

@pytest.mark.main
def test_one_anyon_vac():
    cmds = ['ising', 'anyon1 vac', 'done', 'exit']
    exec(cmds)

@pytest.mark.main
def test_one_anyon_sigma():
    cmds = ['ising', 'anyon1 sigma', 'done', 'exit']
    exec(cmds)

@pytest.mark.main
def test_one_anyon_psi():
    cmds = ['ising', 'anyon1 psi', 'done', 'exit']
    exec(cmds)

@pytest.mark.main
def test_two_anyons():
    cmds = ['ising', 'anyon1 psi', 'anyon2 vac', 'done', 'exit']
    exec(cmds)

@pytest.mark.main
def test_three_anyons():
    cmds = ['ising', 'anyon1 vac', 'anyon2 sigma', 'anyon3 sigma', 'done', 'exit']
    exec(cmds)

@pytest.mark.main
def test_four_anyons():
    cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 psi', 'anyon4 psi', 'done', 'exit']
    exec(cmds)

@pytest.mark.main
def test_list_one_anyon():
    cmds = ['ising', 'anyon1 psi', 'done', 'list', 'exit']
    exec(cmds)

@pytest.mark.main
def test_list_three_anyons():
    cmds = ['ising', 'anyon1 psi', 'anyon2 psi', 'anyon3 vac', 'done', 'list', 'exit']
    exec(cmds)

@pytest.mark.main
def test_fusion_command():
    cmds = ['ising', 'anyon1 psi', 'anyon2 sigma', 'done', 'fusion anyon1 anyon2', 'exit']
    exec(cmds)

@pytest.mark.main
def test_braid_and_print():
    cmds = ['ising', 'anyon1 psi', 'anyon2 sigma', 'anyon3 psi', 'done', 'braid swap anyon1 anyon2', 'braid print', 'exit']
    exec(cmds)

@pytest.mark.main
def test_help_command():
    cmds = ['ising', 'anyon1 psi', 'done', 'help', 'exit']
    exec(cmds)

# @pytest.mark.main
# def test_shell():
#     with patch('subprocess.run') as mock_run:
#         shell = SimulatorShell()
#         shell.do_shell('echo Let\'s go, Brandon!')
#         mock_run.assert_called_once_with('echo Hello, World!', shell=True)
