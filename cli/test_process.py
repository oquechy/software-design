import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from cli.process import CustomProcess, Echo, Pwd, Exit, Cat, Wc, Assignment


class TestProcess(TestCase):
    def test_custom_process(self):
        process = CustomProcess("echo", ["hello", "kitty"])
        output = process.run(None, {})
        self.assertEqual("hello kitty", output)

        process = CustomProcess("python", [])
        output = process.run("print(1 + 1)", {})
        self.assertEqual("2", output)

    def test_echo(self):
        process = Echo(["hello", "kitty"])
        output = process.run(None, {})
        self.assertEqual("hello kitty", output)

        process = Echo([])
        output = process.run("input", {})
        self.assertEqual("", output)

    def test_pwd(self):
        pwd = os.getcwd()

        process = Pwd([])
        output = process.run(None, {})
        self.assertEqual(pwd, output)

        process = Pwd(["a", "b", "c"])
        output = process.run(None, {})
        self.assertEqual(pwd, output)

        process = Pwd([])
        output = process.run("abc", {})
        self.assertEqual(pwd, output)

    def test_cat(self):
        process = Cat([])
        output = process.run("kitty", {})
        self.assertEqual("kitty", output)

        with TemporaryDirectory() as dir:
            with open(dir + "/test", "w") as f:
                f.write("hello kitty")

            process = Cat([f.name])
            output = process.run(None, {})
            self.assertEqual("hello kitty", output)

            process = Cat([f.name])
            output = process.run("world", {})
            self.assertEqual("hello kitty", output)

    def test_wc(self):
        process = Wc([])
        output = process.run("hello\nkitty", {})
        self.assertEqual("2 2 11", output)

        with TemporaryDirectory() as dir:
            with open(dir + "/test", "w") as f:
                f.write("hello\nkitty")

            process = Wc([f.name])
            output = process.run(None, {})
            self.assertEqual("2 2 11", output)

            process = Wc([f.name])
            output = process.run("world", {})
            self.assertEqual("2 2 11", output)

    def test_assignment(self):
        scope = {}
        process = Assignment(["hello", "kitty"])
        process.run(None, scope)
        self.assertEqual(scope, {"hello": "kitty"})

        scope = {"hello": "world"}
        process = Assignment(["hello", "kitty"])
        process.run(None, scope)
        self.assertEqual(scope, {"hello": "kitty"})

    def test_exit(self):
        process = Exit([])
        output = process.run(None, {})
        self.assertEqual("", output)
