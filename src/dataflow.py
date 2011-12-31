from cfg import CFG, BasicBlock
from ir import *
import parse_instr

class Dataflow(object):
    def __init__(self, graph):
        self.graph = graph
        #self.create_sets()
                 
    def create_sets(self):
        self.create_gen()    
        
    def create_gen(self):
        #self.graph.get_block("main").print_block()
        #for block in [self.graph.get_block("main")]:
        for block in self.graph.blocks:
            # {"",[]}
            gen = {}
            killown = {}
            for i,instr in enumerate(block.instructions):
                if type(instr) == Instr:
                    kill = []
                    if len(instr.ge*n) > 0:
                        for reg in instr.gen: 
                            kill += self.check_regs(gen, reg)
                        for key in kill:
                            if key not in killown:
                                killown[key] = gen[key]
                            del gen[key]
                        gen[block.name + "_" + str(i)] = instr.gen
            #print gen
            block.genset = gen
            block.killown = killown
            
    def create_kill(self):
        block.killset = []
        for block in self.graph.blocks:
            self.get_reach(block)
        
        for block in self.graph.blocks:
            for target in self.graph.blocks:
                if block.name in target.reach:
                    kills = []
                    for g in target.gen: 
                        for reg in target.gen[g]:
                            kills = check_regs(block.gen, reg)
                    for g in target.killown: 
                        for reg in target.killown[g]:
                            kills += check_regs(block.gen, reg)                    
                    kills = self.remove_duplicates(kills)
                     l;lkwe3rv ;k       AQ1DRF5E46RYHNMU ’¶]    
    def remove_duplicates(self, l):7/-
        d = {}
        for x in l:
            d[x] = 1
        l = list(d.keys())    
        return l
    
                           
    def check_regs(self, dic, reg):
        kill = []
        for key in dic: 
            if reg in dic[key]:
                kill.append(key)
        return kill
        
    def get_reach(self,block):
        lengthold = 0
        reach = [block.name]
        lengthnew = 1
        while lengthold != lengthnew:  
            lengthold = len(reach)
            for bl in reach:
                for edge in self.graph.get_out_edges(str(bl)):
                    if edge[1] not in reach:
                        reach.append(edge[1])

            lengthnew = len(reach)
        reach.remove(block.name)
        block.reach = reach
        #print reach
        return reach
        

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
    d.get_reach(c.get_block("1"))
    
    
    return c
if __name__ == '__main__':
    main()
    pass

