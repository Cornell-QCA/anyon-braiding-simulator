# Standard Library
import cmd
import sys

from anyon_braiding_simulator.anyon_braiding_simulator import (
    Anyon,
    AnyonModel,
    FibonacciTopoCharge,
    Fusion,
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
                '\nError: you have already provided an anyon in 2D space, so the rest must also have a specified 2D position'
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
                '\nError: you have already provided an anyon in 1D space, so the positions of the rest cannot be specified in 2D'
            )
            return

        try:
            position = tuple(map(float, args[2].replace('{', '').replace('}', '').split(',')))
            if len(position) != 2:
                raise ValueError
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
            print(f'\nCreated anyon {name} with TC {topological_charge} at position {position[0]} in 1D.')
        else:
            print(f'\nCreated anyon {name} with TC {topological_charge} at position {position} in 2D.')
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
        if len(args) < 2:
            print('Error: Not enough arguments for swap')
            return
        
        # Parse the anyon name pairs and convert to indices
        try:
            anyon_pairs = [tuple(anyon.replace('-', ' ').split()) for anyon in args[1:]]
            anyon_indices = sim.pairs_to_indices(anyon_pairs)
        except ValueError:
            print('\nError: A given anyon name does not exist in the simulator.')
            return

        # Perform the swap operations
        braid.swap(anyon_indices)
    elif cmd.lower() == 'print':
        print(braid)
    else:
        print('Error: Unknown braid command')


class SimulatorShell(cmd.Cmd):
    last_command = ''

    def __init__(self):
        super().__init__()
        self.prompt = '\nsimulator> '

        self.command_options = {
            'anyon': 'anyon <name> <topological charge> <{x,y} coords>',
            'model': 'model <Ising or Fibonacci>',
            'braid': 'braid anyon_name_1-anyon_name_2 ...',
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
                    '\nUse the format "<name> <topological charge> <{x,y}>".\n'
                    '> '
                )
            else:
                user_input = input('\nContinue adding anyons (at least 3 total), or type "done" when finished initializing.\n' '> ')

            if user_input.lower() == 'exit':
                sys.exit(0)
            elif user_input.lower() == 'done' and len(sim.list_anyons()) >= 3:
                sim._fusion = Fusion(sim.get_state())
                sim._braid = Braid(sim.get_state(), sim.get_model())
                break
            elif user_input.lower() == 'done' and len(sim.list_anyons()) < 3:
                print('\nError: At least 3 anyons are required to initialize the simulation.')
                continue

            # Check for 2D position in input such that space is allowed (ex. {4, 5})
            if '{' in user_input and '}' in user_input:
                start = user_input.find('{')
                end = user_input.find('}') + 1
                coords = user_input[start:end]

                mod_input = user_input.replace(coords, "COORDS_PLACEHOLDER")
                args = mod_input.split()
                # Replace placeholder with original coords (spaces removed)
                args[args.index("COORDS_PLACEHOLDER")] = coords.replace(" ", "")
            else:
                args = user_input.split(' ')

            if len(args) < 2 or len(args) > 3:
                print('Error: There should be either 2 or 3 arguments')
                continue

            anyon(*args)
            no_anyons = False

        self.init_complete = True

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
        cmds = ['braid', 'exit', 'list']
        print(f'\nCommands: {", ".join(sorted(cmds))}')


if __name__ == '__main__':
    shell = SimulatorShell()
    shell.cmdloop()
