import sys
import re
from collections import defaultdict
import argparse
#Default to an 8 bit cell_size, if you try to use the 'wrong' cell size
#some programs will not behave correctly
def set_cell_size(bits = 8):
    global cell_size, max_value
    cell_size = bits
    max_value = 2 ** cell_size - 1

#do we write -1 to the cell on EOF
write_eof = False

def run(data, data_ptr, cmd):
    if cmd == ">":
        data_ptr += 1
    elif cmd == "<":
        data_ptr -= 1
    elif cmd == "+":
        data[data_ptr] += 1
        if data[data_ptr] == max_value + 1:
            data[data_ptr] = 0
    elif cmd == "-":
        data[data_ptr] -= 1
        if data[data_ptr] == -1:
            data[data_ptr] = max_value
    elif cmd == ".":
        sys.stdout.write(chr(data[data_ptr]))
    elif cmd == ",":
        v = sys.stdin.read(1)
        if v:
            data[data_ptr] = ord(v) 
        elif write_eof:
            data[data_ptr] = -1
    return data_ptr


def brainfuck(program, data = None):
    program = clean(program)
    #use a defaultdict so the 'data' can grow arbitrarily in either direction
    #I haven't tested to see what the speed implications are of this choice
    data = data if data is not None else defaultdict(int)
    cmd_ptr, data_ptr, loops = 0, 0, []
    while cmd_ptr < len(program):
        cmd = program[cmd_ptr]
        if cmd == "[":
            if data[data_ptr]:
                loops.append(cmd_ptr)
            else:
                cmd_ptr = find_matching_brace(program, cmd_ptr)
        elif cmd == "]":
            n = loops.pop()
            if data[data_ptr]:
                cmd_ptr = n - 1
        else:
            data_ptr = run(data, data_ptr, cmd)
        cmd_ptr += 1

def find_matching_brace(program, i):
    open_braces = 1
    while open_braces:
        i += 1
        cmd = program[i]
        if cmd == "[":
            open_braces += 1
        elif cmd == "]":
            open_braces -= 1
    return i

def clean(input):
    p = re.sub(r'[^\[\]><+\-\.,]', '', input, flags = re.M)
    verify(p)
    return p

def verify(program):
    n = 0
    for i in program:
        if i == "[":
            n += 1
        elif i == "]":
            n -= 1
            if n < 0:
                break
    if n:
        raise Exception("Unmatched Braces")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", 
        type = str,
        help = "Path to a BF script or bf code"
    )
    parser.add_argument("-r", "--run",
        action="store_true",
        help = "Run code directly"
    )
    parser.add_argument("-f", "--file",
        action="store_true",
        help = "Execute the contents of a file"
    )
    parser.add_argument("-b", "--bits",
        type = int,
        help = "Set cellsize in bits, default 8",
        default = 8
    )
    parser.add_argument("-e", "--eof",
        action = "store_true",
        help = "Write -1 to cell on EOF",
    )
    args = parser.parse_args()
    set_cell_size(args.bits)
    write_eof = args.eof
    if args.run:
        brainfuck(args.program)
    if args.file:
        with open(args.program) as fh:
            program = fh.read()
        brainfuck(program)
