from cfg import CFG, BasicBlock
from ir import *
import parse_instr

class Dataflow(object):
    def __init__(self, graph):
        self.graph = graph
        self.iterations = 0
        self.set_ins_names()
        self.create_sets()
        
    
    def set_ins_names(self):
        """
        Creates names for instructions, so that they can easily be identified
        during optimisation. Using indexes would cause problems.
        """
        for block in self.graph.blocks:
            for i,instr in enumerate(block.instructions):
                instr.id = block.name + "_" + str(i)
    
    
    def create_sets(self):
        """
        Calls all subroutines to create the different sets in the right order.
        """
        self.create_gen()    
        self.create_kill()
        self.create_inout()
        
    def create_gen(self):
        """
        Determines which instructions are in the gen set of each block
        """
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
                        gen[instr.id] = instr.gen
            block.genset = gen
            block.killown = killown   
            
    def create_kill(self):
        """
        Determines which instructions are in the kill set of each block
        """    
        for block in self.graph.blocks:
            self.get_reach(block)
        
        #For each blokc in the graph
        for block in self.graph.blocks:
            #Check all nodes that can be reached
            for targetname in block.reach:
                target = self.graph.get_block(targetname)
                if target:
                    kills = []
                    
                    #For all instruction in the target block
                    for ins in target.instructions:
                        if type(ins)==Instr:
                            #Check if they write to the same
                            #registers as a instruction in the
                            #origional block
                            for g in ins.gen:
                                kills += self.check_regs(block.genset, g)
                                kills += self.check_regs(block.killown, g)

                    
                    #For all instructions that are overwritten (killed) in the 
                    #origional block, find the corresponding registers and add 
                    #the killed instruction to the killset of the target block.
                    for kill in kills:
                        if kill not in target.killset:
                            if kill in block.genset:
                                target.killset[kill] = block.genset[kill]
                            elif kill in block.killset:
                                target.killset[kill] = block.killown[kill]
    def create_inout(self):
        """
        Determines the in and out sets for blocks using the Iterative algorithm 
        for reaching definitions.
        """
        for block in self.graph.blocks:
            for key in block.genset:
                block.outset[key] = block.genset[key]
        
        change = True
        while change:
            self.iterations += 1
            change = False
            for i,block in enumerate(self.graph.blocks):
            
                #Set inset
                oldin = block.inset
                block.inset = {}
                pred = self.graph.get_in_edges(block)
                for pre in pred:
                    p = self.graph.get_block(pre[0])
                    
                    for key in p.outset:
                        block.inset[key] = p.outset[key]
                #Set outset
                oldout = block.outset
                block.outset =  block.genset
                for key in block.inset:
                    if key not in block.killset:
                        block.outset[key] = block.inset[key]
                #test for change
                #if i == 19:
                #    self.graph.blocks[i].print_block()
                #    print oldout, "\n"
                #    print block.outset, "\n"
                #    print oldin, "\n"
                #    print block.inset, "\n"
                #    print block.killset
                if oldout != block.outset or block.inset != oldin:
                    change = True
    
    def print_sets(self):
        """
        If all sets are determined, they can be printed in a overview for 
        analysis by hand.
        """
        for block in self.graph.blocks:
            print "------------------------------------------------------------"
            block.print_block()
            print "\nGenset:"
            for i in block.genset:
                print str(i) + ": " + str(block.genset[i])                        
            print "\nKillownset:"
            for i in block.killown:
                print str(i) + ": " + str(block.killown[i])   
            print "\nKillset:"
            for i in block.killset:
                print str(i) + ": " + str(block.killset[i])                
            print "\nInset:"
            for i in block.inset:
                print str(i) + ": " + str(block.inset[i])   
            print "\nOutset:"
            for i in block.outset:
                print str(i) + ": " + str(block.outset[i])     
        print "Iterations: ", self.iterations                                  


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
                    if reg == dicreg.expr:
                        kill.append(key)
                elif type(dicreg) == str:
                    if reg == dicreg:
                        kill.append(key)            
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
    for line in open('../benchmarks/slalom.s', 'r').readlines():
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

