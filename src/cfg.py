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

    def __init__(self, instr = None, name = None):
        if not instr:
            self.instructions = []
        else:
            self.instructions = instr
        if name:
            self.name = name
        else:
            self.name = "Nameless"
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
        self.edges = []
        self.blocks = []
        self.load_flat(flat_ir)
        #self.cfg_to_diagram()

        
    def load_flat(self, flat_ir):
        """
        Load list of expression objects in Control Flow Graph.
        """
        self.blocks.append(BasicBlock())
        j = 0
        branches = [
            'beq',   #- branch == 0 
            'bne',   #- branch != 0 
            'blez',  #- branch <= 0 
            'bgtz',  #- branch > 0 
            'bltz',  #- branch < 0 
            'bgez',  #- branch >= 0 
            'bct',   #- branch FCC TRUE 
            'bcf',    #- branch FCC FALSE
            'bc1f',   #- Branch on floating point compare false.
            'bc1t',   #- Branch on floating point compare true.
        ]            
        
        for i,expr in enumerate(flat_ir):
            if (type(expr) == Instr
                and expr.instr in control_instructions
                and not expr.instr in ['jal', 'jalr']):
                self.blocks[-1].append(expr)
                
                # Add edge from this block to the destination of the jump
                try:
                    self.edges.append((self.blocks[-1].name, expr.jump_dest()))
                except exception:
                    print "Adding edge failed because of jump"

                # If previous instruction was a brench, add a edge from the
                # previous block to the new block.
                if (i > 0 and type(flat_ir[i-1]) == Instr
                    and flat_ir[i-1].instr in branches 
                    and len(self.blocks) > 1):
                    self.edges.append((self.blocks[-2].name, self.blocks[-1].name))
                 
                self.blocks.append(BasicBlock(name=str(j)))
                j += 1
            elif type(expr) == Label:
                # If previous instruction wasn't a jump, add an edge between
                # the previous block and the new one.
                if (i > 0 
                    and flat_ir[i-1] not in ['j', 'jr'] 
                    and len(self.blocks) > 1):
                    self.edges.append((self.blocks[-1].name, expr.expr))
                    
                self.blocks.append(BasicBlock([expr], expr.expr))
            else:
                # If previous instruction was a brench, add a edge from the
                # previous block to the new block.                
                if (i > 0 and type(flat_ir[i-1]) == Instr
                    and flat_ir[i-1].instr in branches 
                    and len(self.blocks) > 1):
                    self.edges.append((self.blocks[-2].name, self.blocks[-1].name))
                    
                self.blocks[-1].append(expr)

    def cfg_to_diagram(self):
        import pygraphviz as pgv
        A = pgv.AGraph(directed=True)
        for edge in self.edges: 
            A.add_edge(edge[0], edge[1])
        A.layout()
        A.draw("CFG.png", prog="circo")
    
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
