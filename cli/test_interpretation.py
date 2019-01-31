from unittest import TestCase

from cli.interpretation import interpret
from cli.process import CustomProcess, Echo, Cat, Assignment, Exit, Pwd, Wc


class TestInterpret(TestCase):
    def test_interpret(self):
        processes = interpret(["ls", "-a", "-l", "|", "echo"])
        self.assertEqual([CustomProcess("ls", ["-a", "-l"]), Echo([])], processes)

        processes = interpret(["cat", "kitty.txt", "|", "kitty=hello", "|", "exit"])
        self.assertEqual([Cat(["kitty.txt"]), Assignment(["kitty", "hello"]), Exit([])], processes)

        processes = interpret(["pwd", "|", "wc", "hello.txt"])
        self.assertEqual([Pwd([]), Wc(["hello.txt"])], processes)
   