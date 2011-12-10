#!/usr/bin/env python

#
# cfg.py
#

"""

Control Flow Graph and Basic Block

"""

from ir import Instr, Label, control_instructions



class BasicBlock(object):
    """
    Basic Block

    """

    def __init__(self, instr = None):
        if not instr:
            self.instructions = []
        else:
            self.instructions = instr
        self.next = []


    def __getitem__(self, index):
        return self.instructions[index]


    def __setitem__(self, index, value):
        self.instructions[index] = value


    def __len__(self):
        "Return number of instructions in this block."
        return len(self.instructions)

    def append(self, value):
        "Append instruction to block."
        self.instructions.append(value)

    def __str__(self):
        return str(self.instructions)
    


class CFG(object):
    """
    Control Flow Graph
    
    """
    
    def __init__(self, flat_ir):
        self.blocks = []
        self.load_flat(flat_ir)

        
    def load_flat(self, flat_ir):
        """
        Load list of expression objects in Control Flow Graph.

        """

        self.blocks.append(BasicBlock())
        for expr in flat_ir:
            if (type(expr) == Instr
                and expr.instr in control_instructions
                and not expr.instr in ['jal', 'jalr']):
                self.blocks[-1].append(expr)
                self.blocks.append(BasicBlock())
            elif type(expr) == Label:
                self.blocks.append(BasicBlock([expr]))
            else:
                self.blocks[-1].append(expr)

    
    def cfg_to_flat(self):
        """
        Convert Control Flow Graph to list of expression objects.
        
        """
        
        return sum((list(block) for block in self.blocks), [])

        

if __name__ == '__main__':
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/pi.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    c = CFG(flat)
