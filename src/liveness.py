from cfg import CFG, BasicBlock
from ir import *


class Liveness(object):
    def __init__(self, graph):
        self.graph = graph
        self.dataflow = False
        self.dataflow = dataflow_done()
        if self.dataflow:
            self.analyse()
    
    def dataflow_done(self):
        result = False
        for block in self.graph.blocks:
            if len(block.inset) > 0
                result = True
                break
        return result
    
    def analyse(self):
        self.ana_livein()
    
    def ana_livein(self:
        pass
     

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/whet.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    flat = parse_instr.parse(flat)
    c = CFG(flat)
    d = Dataflow(c)
    
    d.print_sets()
    #d.get_reach(c.get_block("$L7"))
    
    
    return c
if __name__ == '__main__':
    main()
    pass
