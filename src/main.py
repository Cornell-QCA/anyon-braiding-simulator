from functools import partial

def anyon(*args):
    print("anyon")

def model(*args):
    print("model")

def fusion(*args):
    print("fusion")

def braid(*args):
    print("braid")


if __name__ == "__main__":
    while True:
        user_input = input("> ")

        args = user_input.split(' ')
        command = args[0]

        command_options = {
            "anyon": "anyon <name> <topological charge> <{x,y} coords>",
            "model": "model <Ising or Fibonacci>",
            "fusion": "fusion anyon_name_1 anyon_name_2 ...",
            "braid": "braid anyon_name_1 anyon_name_2 ...",
        }

        command_functions = {
            "anyon": anyon,
            "model": model,
            "fusion": fusion,
            "braid": braid,
        }

        if command == "exit":
            break
        elif command == "help":
            print("Commands: anyon, model, fusion, braid, exit, help")

        for cmd in command_options.keys():
            if command == cmd:
                if len(args) == 1:
                    print("Add the -h flag for help with this command")
                elif args[1] == "-h" or args[1] == "--help":
                    print(command_options[cmd])
                else:
                    command_functions[cmd](*args[1:])

        if command not in command_options.keys() and command not in ["exit", "help"]:
            print("Command not found")
