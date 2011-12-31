from cfg import CFG, BasicBlock
from ir import *
import parse_instr

class Dataflow(object):
    def __init__(self, graph):
        self.graph = graph
        self.create_sets()
                 
    def create_sets(self):
        #for bl in self.graph.blocks:
        #    create_gen(bl)
        self.create_gen(self.graph.get_block("main"))    
        self.graph.get_block("main").print_block()
    def create_gen(self,block):
        # {"",[]}
        gen = {}
        for i,instr in enumerate(block.instructions):
            if type(instr) == Instr:
                kill = []
                if len(instr.gen) > 0:
                    for reg in instr.gen: 
                        kill += self.check_regs(gen, reg)
                    for key in kill:
                        del gen[key]     
                    gen[block.name + "_" + str(i)] = instr.gen
        print gen
        return gen
    
    def check_regs(self, dic, reg):
        kill = []
        for key in dic: 
            if reg in dic[key]:
                kill.append(key)
        return kill
        
    
        

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/pi.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    flat = parse_instr.parse(flat)
    c = CFG(flat)
    d = Dataflow(c)    
    
    
    return c
if __name__ == '__main__':
    main()
    pass

