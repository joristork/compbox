from cfg import CFG, BasicBlock
from ir import *
import parse_instr
from dataflow import Dataflow
from itertools import izip

class Liveness(object):
    def __init__(self, graph, verbosity=2):
        self.graph = graph
        self.verbosity = verbosity
        #self.dataflow = False
        #self.dataflow = dataflow_done()
        #if self.dataflow:
        #change = True
        #while change:
        #    self.analyse()
        #    change = self.optimise()
        #    print change
        #self.analyse()
        
    def dataflow_done(self):
        result = False
        for block in self.graph.blocks:
            if len(block.inset) > 0:
                result = True
                break
        return result
    
    def analyse(self):
        atnode = []
        blocknames = []
        for block in self.graph.blocks:
            blocknames.append(block.name) 
            #block.print_block()
            for i in xrange(1,len(block.instructions)):
                if type(block.instructions[-i])==Instr:
                    #print "1, ", block.instructions[-i]
                    needs = []
                    for reg in block.instructions[-i].need:
                        if type(reg)==Register:
                            needs.append(reg)
                    #print "2, ", needs
                    for j in xrange(i + 1, len(block.instructions) + 1):
                        
                        if type(block.instructions[-j])==Instr:
                            #print "3, ", block.instructions[-j]
                            for n in needs:
                                for g in block.instructions[-j].gen:
                                    #print "4, ", repr(g)
                                    if type(g)==Register and n.expr == g.expr:
                                        #print "5, ", n, g, block.instructions[-j].id
                                        if block.instructions[-j].id not in block.live_in_node:
                                            block.live_in_node.append(block.instructions[-j].id)
                                            block.live_in_node_reg += block.instructions[-j].gen
                                        needs.remove(n)
                                        #Register that is needed is set in
                                        #this last instruction. No need to
                                        #look further.
                                        break
                            #Registers that are still in the needs list, are
                            #registers that are not set in the block. They
                            #are in the in set of 
                            #the block.
                    #print "6, ", block.live_in_node
                    #print "7 (needs), ", needs
                    for n in needs:
                        if not self.reg_in_reglist(n, block.livein): #n.expr not in block.livein
                            block.livein.append(n)
                    #print "8 (needs), ", block.livein
                    

              
            if len(self.graph.get_out_edges(block)) == 0 and len(self.graph.get_in_edges(block)) > 0:
                atnode.append(block)
                block.liveout = []


        for edge in self.graph.edges:
            if edge[1] not in blocknames:
                for e in self.graph.get_in_edges(edge[1]):
                    b = self.graph.get_block(e[0])
                    if b: 
                        atnode.append(b)
        passednodes = []              
        while len(atnode) != 0:
            
            copyatnode = atnode[:]
            for block in copyatnode:
                self.remove_block_list(block,atnode)
                for edge in self.graph.get_in_edges(block):
                    #print "test"
                    succ = self.graph.get_block(edge[0])
                    oldout = succ.liveout[:]
                    oldin = succ.livein[:]
                    for inreg in block.livein:
                        if not self.reg_in_reglist(inreg, succ.liveout):
                            succ.liveout.append(inreg)
                        if (not self.reg_in_reglist(inreg, succ.live_in_node_reg)) and (not self.reg_in_reglist(inreg, succ.livein)):
                            succ.livein.append(inreg)
                            
                    if not (self.comp_reglist(oldin, succ.livein) and self.comp_reglist(oldout, succ.liveout) and succ.name in passednodes):
                        atnode.append(succ)
                        passednodes.append(succ.name)
                    
    def comp_reglist(self,a,b):
        if len(a)!=len(b):
            return False
        
        for i in a:
            found = False
            for j in b:
                if i.expr == j.expr:
                    found = True
                    break
            if not found:
                return False
        return True
    
    def remove_block_list(self,b,l):
        for block in l:
            if block.name == b.name:
                l.remove(block)
                
    def reg_in_reglist(self,reg,reglist):
        #print reg, reglist
        for r in reglist:
            if r.expr == reg.expr:
                return True
        return False
        
    def print_live(self):
        for block in self.graph.blocks:
            print "------------------------------------------------------------"
            block.print_block()
            print "\nLive in:"
            for i in block.livein:
                print i  
                
            print "\nLive out:"
            for i in block.liveout:
                print i   

            print "\nKill instructions:"
            for i in block.live_in_node:
                print i                       
                
    def optimise(self):
        # Creates a reversed list and index from a list
        reverse_enumerate = lambda l: izip(xrange(len(l)-1, -1, -1), reversed(l))
        change = False
        # For each block in the graph
        for block in self.graph.blocks:
            clean = False
            while not clean:
                # Create a out list, containing all registers that are needed
                # further in the graph
                out = block.liveout[:]
                clean = True
                # Reverse the instruction list and loop
                for i,ins in reverse_enumerate(block.instructions):
                    if type(ins) == Instr and ins.instr not in ['jal','jalr']:
                        islive = len(ins.gen) == 0
                        # Check if this instruction writes to a register
                        # that is in the out set
                        for ins_gen in ins.gen:
                            index, inlist = self.in_reglist(ins_gen, out)
                            # If that is the case, this instruction is live
                            # and the register in the outset can be removed
                            if inlist:
                                islive = True
                                del out[index]
                        # If the instructions isn't live, it can be removed and
                        # because of list indexes we have to start optimalisation
                        # on this block over again.
                        if not islive:
                            print "Removed: ", ins
                            del block.instructions[i]
                            clean = False
                            break
                        # If the instruction is live, the registers it uses need
                        # to be added tot the out list. 
                        else:
                            for ins_need in ins.need:
                                index, inlist = self.in_reglist(ins_need, out)
                                if not inlist:
                                    out.append(ins_need)
        return change
                    
    def comp_regs(self,a,b):
        """ 
        Checks if there is an item in list a that is also in
        list b
        """
        for reg in a:
            for r in b:
                if reg.expr == r.expr:
                    return True
        return Falsei

    def in_reglist(self, reg, l):
        """ 
        Checks if a register is in a registerlist and return a 
        tuple containing a boolean and a index. 
        """
        for i, r in enumerate(l):
            if type(reg) == Register and type(r) == Register and reg.expr == r.expr:
                return (i, True)
        return (0, False)



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
    l = Liveness(c)
    change = True
    while change:
        l.analyse()
        change = l.optimise()  
    for ins in flat:
        print ins
    #1d.print_sets()
    #d.get_reach(c.get_block("$L7"))
    
    
    return c
if __name__ == '__main__':
    main()
    pass
