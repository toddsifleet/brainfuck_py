import unittest
import brainfuck
import sys
from StringIO import StringIO


def run_program(program, input = None):
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    try:
        out = StringIO()
        sys.stdout = out
        if input is not None:
            input = StringIO(input) 
            sys.stdin = input
        brainfuck.brainfuck(program)
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin

    return out.getvalue().strip()

class TestInterpreter(unittest.TestCase):
    def setUp(self):

        brainfuck.set_cell_size()

    def test_HelloWorld(self):
        result = run_program("""
                    ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.
                    +++++++..+++.>++.<<+++++++++++++++.>.+++.------.-
                    -------.>+.>.""")
        self.assertEquals(result, "Hello World!")
    def test_Squares(self):
        result = run_program("""
                    ++++[>+++++<-]>[<+++++>-]+<+[>[>+>+<<-]++>>[<<+>>
                    -]>>>[-]++>[-]+>>>+[[-]++++++>>>]<<<[[<++++++++<+
                    +>>-]+<.<[>----<-]<]<<[>>>>>[>>>[-]+++++++++<[>-<
                    -]+++++++++>[-[<->-]+[<<<]]<[>+<-]>]<<-]<<-]""")
        expected_result = "\n".join([str(x**2) for x in range(101)])
        self.assertEquals(result, expected_result)

    def test_ROT13(self):
        result = run_program("""
                    -,+[-[>>++++[>++++++++<-]<+<-[>+>+>-[>>>]<[[>+<-]
                    >>+>]<<<<<-]]>>>[-]+>--[-[<->+++[-]]]<[++++++++++
                    ++<[>-[>+>>]>[+[<+>-]>+>>]<<<<<-]>>[<+>-]>[-[-<<[
                    -]>>]<<[<<->>-]>>]<<[<<+>>-]]<[-]<.[-]<-,+]""", "applesauce")
        self.assertEquals(result, "nccyrfnhpr")
    
    def test_Clean(self):
        self.assertRaises(Exception, brainfuck.clean, "[[]")
        self.assertRaises(Exception, brainfuck.clean, "][")
if __name__ == '__main__':
    unittest.main()
