import cmd
from Simulator import Simulator

sim = Simulator()

def anyon(*args):
    '''
    Handle the anyon command. This command adds an anyon to the simulation.
    '''
    if len(args) < 3:
        print("Error: Not enough arguments")
        return

    name = args[0]

    try:
        topological_charge = float(args[1])
    except ValueError:
        print("Error: topological charge must be a number")
        return

    try:
        position = tuple(map(float, args[2].replace("{", "").replace("}", "").split(",")))
    except ValueError:
        print("Error: position must be formatted as {x, y} where x and y are numbers")
        return

    # waiting on Anyon class
    # anyon = Anyon(name, topological_charge, position)
    # sim.update_anyons(True, [anyon])

    print(f"Created anyon {name} with TC {topological_charge} at position {position}")

def model(*args):
    '''
    Handle the model command. This command sets the model for the simulation.
    '''
    print("model")

def fusion(*args):
    '''
    Handle the fusion command. This command fuses anyons together.
    '''
    print("fusion")

def braid(*args):
    '''
    Handle the braid command. This command braids anyons together.
    '''
    print("braid")


class SimulatorShell(cmd.Cmd):

    last_command = ""

    def __init__(self):
        super().__init__()
        self.prompt = "simulator> "

        self.command_options = {
            "anyon": "anyon <name> <topological charge> <{x,y} coords>",
            "model": "model <Ising or Fibonacci>",
            "fusion": "fusion anyon_name_1 anyon_name_2 ...",
            "braid": "braid anyon_name_1 anyon_name_2 ...",
        }

    def do_shell(self, arg):
        "Run a shell command"
        print("running shell command:", arg)
        import subprocess
        subprocess.run(arg, shell=True)

    def do_anyon(self, arg):
        "Add an anyon to the simulation"
        args = arg.split(' ')
        if args[0] == "help" or args[0] == "-h":
            print(self.command_options["anyon"])
        else:
            anyon(*args)


    def do_model(self, arg):
        "Set the model for the simulation"
        args = arg.split(' ')
        model(*args)
        if args[0] == "help" or args[0] == "-h":
            print(self.command_options["model"])
        else:
            model(*args)


    def do_fusion(self, arg):
        "Fuse anyons together"
        args = arg.split(' ')
        if args[0] == "help" or args[0] == "-h":
            print(self.command_options["fusion"])
        else:
            fusion(*args)

    def do_braid(self, arg):
        "Braid anyons together"
        args = arg.split(' ')
        if args[0] == "help" or args[0] == "-h":
            print(self.command_options["braid"])
        else:
            braid(*args)

    def do_exit(self, arg):
        "Exit the simulator"
        return True

    def do_help(self, arg):
        "Print help"
        print("Commands: anyon, model, fusion, braid, exit, help")

if __name__ == "__main__":
    shell = SimulatorShell()
    shell.cmdloop()
