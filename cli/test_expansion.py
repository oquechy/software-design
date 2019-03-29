from unittest import TestCase
from cli.expansion import expand, State


class TestExpand(TestCase):

    def test_expand(self):
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a"]), expand("ls -a", {}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a", "|", "tee"]), expand("ls -a | tee", {}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a"]), expand("'l's -\"a\"", {}))
        self.assertEqual((State.BARE_STRING, "", ["ls -a"]), expand("l's -'a", {}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a"]), expand("ls   -a  ", {}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a"]), expand("ls -a", {}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a"]), expand("ls -$b", {"b": "a"}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-la"]), expand("$ts -$b", {"b": "la", "t": "l", "ts": "www"}))
        self.assertEqual((State.BARE_STRING, "", ["cat", "-la"]), expand("$ts -$b", {"b": "la", "ts": "cat"}))
        self.assertEqual((State.BARE_STRING, "", ["l$s \" -$b"]), expand("'l$s \" -$b'", {"b": "la", "s": "cat"}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-la"]), expand("\"l$t\" -\"$b\"", {"b": "la", "t": "s"}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-la'"]), expand("\"l$t\" -\"$b'\"", {"b": "la", "t": "s"}))
        self.assertEqual((State.BARE_STRING, "", ["ls", "-a"]), expand("ls'' -a", {}))
        self.assertEqual((State.DOUBLE_QUOTE, "-a\n", ["ls"]), expand("ls'' -\"a", {}))
        self.assertEqual((State.SINGLE_QUOTE, "ls -a\n", []), expand("ls''' -a", {}))
