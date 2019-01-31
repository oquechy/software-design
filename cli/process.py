import os
import subprocess
from abc import abstractmethod, ABC


class Process(ABC):
    """Base class for cli commands."""

    def __init__(self, command, args):
        self.command = command
        self.args = args

    @abstractmethod
    def run(self, input, scope):
        pass

    def __eq__(self, other):
        return isinstance(other, Process) and other.command == self.command and other.args == self.args


class CustomProcess(Process):
    """Runs custom shell script."""

    def __init__(self, command, args):
        super().__init__(command, args)

    def run(self, input, scope):
        command = [self.command] + self.args
        result = subprocess.run(command, stdout=subprocess.PIPE, input=input, universal_newlines=True, check=True)
        return result.stdout.rstrip()


class Echo(Process):
    """Returns it's arguments separated by spaces."""

    def __init__(self, args):
        super().__init__("echo", args)

    def run(self, input, scope):
        return " ".join(self.args)


class ArgumentError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Cat(Process):
    """Accepts a filename as an argument and returns it's contents. Can use piped input if file is not given."""

    def __init__(self, args):
        super().__init__("cat", args)

    def run(self, input, scope):
        if len(self.args) == 1:
            with open(self.args[0]) as f:
                return f.read()
        elif not self.args and input is not None:
            return input
        else:
            raise ArgumentError(self.__doc__)


class Wc(Process):
    """Accepts a filename as an argument and returns number of lines, words and symbols in it.
    Can use piped input if file is not given."""

    def __init__(self, args):
        super().__init__("wc", args)

    def run(self, input, scope):
        if not self.args and input is None or len(self.args) > 1:
            raise ArgumentError(self.__doc__)

        if self.args:
            with open(self.args[0]) as f:
                input = f.read()
        return " ".join(str(len(units)) for units in [input.split("\n"), input.split(), input])


class Exit(Process):
    """Shuts down cli."""

    def __init__(self, args):
        super().__init__("exit", args)

    def run(self, input, scope):
        if self.args:
            raise ArgumentError(self.__doc__)
        return ""


class Pwd(Process):
    """Prints a path of the current working directory."""

    def __init__(self, args):
        super().__init__("pwd", args)

    def run(self, input, scope):
        return os.getcwd()


class Assignment(Process):
    """Assigns a value to an environment variable."""

    def __init__(self, args):
        super().__init__("=", args)

    def run(self, input, scope):
        if len(self.args) != 2:
            raise ArgumentError(__doc__)
        scope[self.args[0]] = self.args[1]
        return ""
