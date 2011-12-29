from cfg import CFG, BasicBlock
from ir import *


class Dataflow(object):
    def __init__(self, graph):
        self.graph = graph
        
    def get_genset(block):
        for instr in block.instructions:
            if type(instr) == Instr:
                 
    
    def create_sets(self,blocks):

                    
        

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/pi.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    c = CFG(flat)
    d = Dataflow(c)    
    
    
    return c
if __name__ == '__main__':
    main()
    pass

