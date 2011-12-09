#
# Control Flow Graph
#

from ir import *



class BasicBlock(object):
    """   """

    def __init__(self, instructions=[]):
        self.instructions = instructions
        self.next = []


    def __getitem__(self, index):
        """   """
        
        return self.instructions[index]


    def __setitem__(self, index, value):
        """   """

        self.instructions[index] = value


    def __len__(self):
        """   """
        return len(self.instructions)

    def append(self, value):
        self.instructions.append(value)

    def __str__(self):
        return str(self.instructions)
    


class CFG(object):
    def __init__(self, flat_ir):
        self.blocks = []
        self.load_flat(flat_ir)
        
    def load_flat(self, flat_ir):

        labels = {}
        block = BasicBlock()
        self.blocks.append(block)
        for expr in flat_ir:
            if type(expr) == Instr and expr.instr in control_instructions:
                block.append(expr)
                
                block = BasicBlock()
                self.blocks.append(block)
            elif type(expr) == Label:
                
                block = BasicBlock([expr])
                self.blocks.append(block)
            else:
                block.append(expr)
    
    def cfg_to_flat(self):
        reduce( lambda x,y: x+y,  [list(block) for block in self.blocks], [])

        

if __name__ == '__main__':
     from asmyacc import parser
     c = CFG([parser.parse(line) for line in open('../benchmarks/pi.s', 'r').readlines()])
