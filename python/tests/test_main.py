# Standard Library
import os

import pytest
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
def test_join():
    cmds = ['ising', 'exit']
    exec(cmds)


@pytest.mark.main
def test_fusion():
    cmds = ['ising', 'anyon psi 0 0', 'anyon sigma 1 0', 'fusion 0 1', 'exit']
    exec(cmds)
