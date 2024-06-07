# Standard Library
import cmd
import subprocess

from Anyon import Anyon
from Braiding import Braid
from Model import AnyonModel, Model
from Simulator import Simulator

sim = Simulator()


def anyon(*args):
    """
    Handle the anyon command. This command adds an anyon to the simulation.
    """
    if len(args) < 3:
        print('Error: Not enough arguments')
        return

    name = args[0]

    try:
        topological_charge = float(args[1])
    except ValueError:
        print('Error: topological charge must be a number')
        return

    try:
        position = tuple(map(float, args[2].replace('{', '').replace('}', '').split(',')))
        position[1]
    except ValueError:
        print('Error: position must be formatted as {x, y} where x and y are numbers')
        return
    except IndexError:
        print('Error: position must be formatted as {x, y} where x and y are numbers')
        return

    new_anyon = Anyon(topological_charge, name, position)
    sim.update_anyons(True, [new_anyon])

    print(f'Created anyon {name} with TC {topological_charge} at position {position}')


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

    braid = Braid(sim.list_anyons())
    cmd = args[0]

    if cmd.lower() == 'swap':
        braid.swap(args[1], args[2])
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

    def do_shell(self, arg):
        "Run a shell command"
        print('running shell command:', arg)
        subprocess.run(
            arg,
            shell=True,
        )

    def do_anyon(self, arg):
        "Add an anyon to the simulation"
        args = arg.split(' ')
        if args[0] == 'help' or args[0] == '-h':
            print(self.command_options['anyon'])
        else:
            anyon(*args)

    def do_model(self, arg):
        "Set the model for the simulation"
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
            print(sim.list_anyons())

    def do_exit(self, arg):
        "Exit the simulator"
        return True

    def do_help(self, arg):
        "Print help"
        print('Commands: anyon, model, fusion, braid, exit, help')


if __name__ == '__main__':
    shell = SimulatorShell()
    shell.cmdloop()
