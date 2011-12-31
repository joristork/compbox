from cfg import CFG, BasicBlock
from ir import *
import parse_instr

class Dataflow(object):
    def __init__(self, graph):
        self.graph = graph
        self.create_sets()
                 
    def create_sets(self):
        self.create_gen()    
        
    def create_gen(self):
        """
        Determines which instruction are in the gen set of each block
        """
        #self.graph.get_block("$L4").print_block()
        #for block in [self.graph.get_block("$L4")]:
        for block in self.graph.blocks:
            # {"",[]}
            gen = {}
            killown = {}
            for i,instr in enumerate(block.instructions):
                if type(instr) == Instr:
                    kill = []
                    if len(instr.gen) > 0:
                        for reg in instr.gen: 
                            kill += self.check_regs(gen, reg)
                        for key in kill:
                            if key not in killown:
                                killown[key] = gen[key]
                            if key in gen:
                                del gen[key]
                        gen[block.name + "_" + str(i)] = instr.gen
            block.genset = gen
            block.killown = killown   
            
    def create_kill(self):
        block.killset = []
        for block in self.graph.blocks:
            self.get_reach(block)
        
        for block in self.graph.blocks:
            for targetname in block.reach:
                target = self.graph.get_block(targetname)
                kills = []
                
                
                #for g in target.gen: 
                #    for reg in target.gen[g]:
                #        kills = check_regs(block.gen, reg)
                #for g in target.killown: 
                #    for reg in target.killown[g]:
                #        kills += check_regs(block.gen, reg)  
                                          
                kills = self.remove_duplicates(kills)
                for kill in kills:
                    if kill not in target.killset:
                        if kill in block.gen:
                            target.killset[key] = block.gen[key]
                        elif kill in block.killown:
                            target.killset[key] = block.gen[key]                            
                            

    def remove_duplicates(self, l):
        """
        Removes all duplicate values in a list (with hashable values)
        """
        d = {}
        for x in l:
            d[x] = 1
        l = list(d.keys())    
        return l
    
                           
    def check_regs(self, dic, reg):
        """
        Checks if the register that is given, is in the gen dict of
        a block. If
        so, the key (instruction name) is added to a list and
        returned.
        """
        kill = []
        if type(reg) == Register:
            reg = reg.expr
        for key in dic: 
            for dicreg in dic[key]:
                if type(dicreg) == Register:
                    #print reg, dicreg.expr, reg==dicreg.expr
                    if reg == dicreg.expr:
                        kill.append(key)
                elif type(dicreg) == str:
                    #print reg, dicreg
                    if reg == dicreg:
                        kill.append(key)    
        #print kill            
        return kill
        
    def get_reach(self,block):
        """
        Returns a list that contains all names of the blocks that can
        be reached from the given block.
        
        Example: Graph = b1 -> b2 -> b3 Reach(b1) = [b2,b3]
        """
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
    d.get_reach(c.get_block("$L7"))
    
    
    return c
if __name__ == '__main__':
    main()
    pass

