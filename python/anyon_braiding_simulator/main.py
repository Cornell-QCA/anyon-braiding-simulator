# Standard Library
import cmd
import subprocess
import sys

from anyon_braiding_simulator.anyon_braiding_simulator import (
    Anyon,
    AnyonModel,
    FibonacciTopoCharge,
    IsingTopoCharge,
    TopoCharge,
)
from Braiding import Braid
from Model import Model
from Simulator import Simulator

sim = Simulator()


def anyon(*args):
    """
    Handle the anyon command. This command adds an anyon to the simulation.
    """
    if len(args) != 2 and len(args) != 3:
        print('Error: There should be either 2 or 3 arguments')
        return

    name = args[0]
    topological_charge = args[1]
    position = ()

    topo_charge = {}
    if sim.get_model().get_model_type() == AnyonModel.Ising:
        topo_charge = {
            'psi': IsingTopoCharge.Psi,
            'sigma': IsingTopoCharge.Sigma,
            'vac': IsingTopoCharge.Vacuum,
        }
    elif sim.get_model().get_model_type() == AnyonModel.Fibonacci:
        topo_charge = {
            'tau': FibonacciTopoCharge.Tau,
            'Vacuum': FibonacciTopoCharge.Vacuum,
        }
    else:
        print('Error: Model not set')
        return

    try:
        topological_charge = topo_charge[args[1].lower()]
    except KeyError:
        print(f'Error: topological charge must be in {list(topo_charge.keys())}')
        return

    if len(args) == 2:
        anyons = sim.list_anyons()
        # Make sure any previous anyons were specified in 1D space (i.e. without a position argument)
        if anyons and sim.get_dim_of_anyon_pos() == 2:
            print(
                'Error: you have already provided an anyon in 2D space, so the rest must also have a \
                    specified 2D position'
            )
            return
        elif not anyons:
            sim.switch_to_1D()

        position_1D = len(anyons)  # Index/position of new anyon in 1D
        position = (position_1D, 0)
    else:
        # Make sure any previous anyons were specified in 2D space
        if sim.get_dim_of_anyon_pos() == 1:
            print(
                'Error: you have already provided an anyon in 1D space, so the positions of the rest \
                    cannot be specified in 2D'
            )
            return

        try:
            position = tuple(map(float, args[2].replace('{', '').replace('}', '').split(',')))
            position[1]
        except ValueError:
            print('Error: position must be formatted as {x,y} where x and y are numbers')
            return
        except IndexError:
            print('Error: position must be formatted as {x,y} where x and y are numbers')
            return

    new_anyon = Anyon(name, TopoCharge(topological_charge), position)
    try:
        sim.update_anyons(True, [new_anyon])
        if len(args) == 2:
            print(f'Created anyon {name} with TC {topological_charge} at position {position[0]} in 1D')
        else:
            print(f'Created anyon {name} with TC {topological_charge} at position {position} in 2D')
    except ValueError:
        print('Error: An anyon with the same name already exists')


def model(*args):
    """
    Handle the model command. This command sets the model for the simulation.
    """

    if len(args) < 1:
        print('Error: Not enough arguments')
        return

    model_type = str(args[0])
    if model_type.lower() != 'ising' and model_type.lower() != 'fibonacci':
        print('Error: Model must be Ising or Fibonacci')
        return

    model_convert = {'ising': AnyonModel.Ising, 'fibonacci': AnyonModel.Fibonacci}

    model = Model(model_convert[model_type.lower()])
    sim.set_model(model)


def fusion(*args):
    """
    Handle the fusion command. This command executes the various fusion operations.
    """
    if len(args) < 1:
        print('Error: Not enough arguments')
        return

    # fusion = Fusion()
    cmd = args[0]

    if cmd.lower() == 'fuse':
        # anyon_indices = [sim.list_anyons().index(anyon) for anyon in args[1:]]
        # fusion.fuse(*anyon_indices)
        pass

    elif cmd.lower() == 'print':
        # print(fusion)
        pass
    else:
        print('Error: Unknown fusion command')


def braid(*args):
    """
    Handle the braid command. This command executes the various braid operations.
    """

    if len(args) < 1:
        print('Error: Not enough arguments')
        return

    braid = sim._braid
    cmd = args[0]

    if cmd.lower() == 'swap':
        index_A, index_B = sim.get_anyon_index(args[2], args[3])
        swap = [(index_A, index_B)]
        # swaps = [tuple(map(int, swap.replace('(', '').replace(')', '').split(','))) for swap in args[2].strip('[]').split('),(')]
        braid.swap(int(args[1]), swap)
    elif cmd.lower() == 'print':
        print(braid)
    else:
        print('Error: Unknown braid command')


class SimulatorShell(cmd.Cmd):
    last_command = ''

    def __init__(self):
        super().__init__()
        self.prompt = 'simulator> '

        self.command_options = {
            'anyon': 'anyon <name> <topological charge> <{x,y} coords>',
            'model': 'model <Ising or Fibonacci>',
            'fusion': 'fusion anyon_name_1 anyon_name_2 ...',
            'braid': 'braid anyon_name_1 anyon_name_2 ...',
            'list': 'list',
        }

        # Flag to indicate whether initialization (model & anyon choice) is completed
        self.init_completed = False

        # Prompt the user to input the anyon model
        while True:
            user_input = input('Enter the anyon model ("ising" or "fibonacci"): ')
            if user_input.lower() == 'ising' or user_input.lower() == 'fibonacci':
                break
            elif user_input.lower() == 'exit':
                sys.exit(0)
            else:
                print('\nError: Invalid model.')

        model(user_input)

        # Prompt the user to input the anyon details
        no_anyons = True
        while True:
            if no_anyons:
                user_input = input(
                    '\nEnter the anyon name, topological charge, and optionally, the 2D position.'
                    '\nUse the format <name> <topological charge> <{x,y}>.\n'
                    '> '
                )
            else:
                user_input = input('\nContinue adding anyons, or type "done" when finished initializing.\n' '> ')

            if user_input.lower() == 'exit':
                sys.exit(0)
            elif user_input.lower() == 'done':
                sim._braid = Braid(sim.get_state(), sim.get_model())
                break

            args = user_input.split(' ')
            if len(args) < 2 or len(args) > 3:
                print('Error: There should be either 2 or 3 arguments')
                continue

            anyon(*args)
            no_anyons = False

        self.init_complete = True

    def do_shell(self, arg):
        "Run a shell command"
        print('running shell command:', arg)
        subprocess.run(
            arg,
            shell=True,
        )

    def do_anyon(self, arg):
        "Add an anyon to the simulation"
        if self.init_complete:
            print('Error: Cannot add anyons after initialization')
            return

        args = arg.split(' ')
        if args[0] == 'help' or args[0] == '-h':
            print(self.command_options['anyon'])
        else:
            anyon(*args)

    def do_model(self, arg):
        "Set the model for the simulation"
        if self.init_complete:
            print('Error: Cannot change model after initialization')
            return

        args = arg.split(' ')
        model(*args)
        if args[0] == 'help' or args[0] == '-h':
            print(self.command_options['model'])
        else:
            model(*args)

    def do_fusion(self, arg):
        "Fuse anyons together"
        args = arg.split(' ')
        if args[0] == 'help' or args[0] == '-h':
            print(self.command_options['fusion'])
        else:
            fusion(*args)

    def do_braid(self, arg):
        "Braid anyons together"
        args = arg.split(' ')

        if args[0].lower() == 'help' or args[0].lower() == '-h':
            print(self.command_options['braid'])
        else:
            braid(*args)

    def do_list(self, arg):
        "Lists anyons present"
        args = arg.split(' ')
        if args[0] == 'help' or args[0] == '-h':
            print(self.command_options['list'])
        else:
            print(f'Anyons: {"\n\t".join([str(anyon) for anyon in sim.list_anyons()])}')

    def do_exit(self, arg):
        "Exit the simulator"
        return True

    def do_help(self, arg):
        "Print help"
        cmds = ['anyon', 'model', 'fusion', 'braid', 'exit', 'list']
        print(f'Commands: {", ".join(sorted(cmds))}')


if __name__ == '__main__':
    shell = SimulatorShell()
    shell.cmdloop()
