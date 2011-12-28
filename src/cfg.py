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
        """
        Sets the blocks and edges, by executing the load_flat function. The
        load_flat function gets of (flat) list of instructions.
        After the edges and blocks are found a png image is generated that
        displays the cfg.
        """
        #The edges of the graph are tuples, where the first value is the
        #name of the source node and the second value is the name of the
        #destination node.
        self.edges = []
        self.blocks = []
        self.load_flat(flat_ir)
        self.cfg_to_diagram()

        
    def load_flat(self, flat_ir):
        """
        Load list of expression objects in Control Flow Graph.
        """
        self.blocks.append(BasicBlock())
        j = 0
        brenches = [
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
                    and flat_ir[i-1].instr in brenches 
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
                    and flat_ir[i-1].instr in brenches 
                    and len(self.blocks) > 1):
                    self.edges.append((self.blocks[-2].name, self.blocks[-1].name))
                    
                self.blocks[-1].append(expr)

    def cfg_to_diagram(self):
        """
        Generates a diagram using the edges that were found when load_flat
        was executed. The result is saved in a png image file.
        """
        import pygraphviz as pgv
        A = pgv.AGraph(directed=True)
        for edge in self.edges: 
            A.add_edge(edge[0], edge[1])
        A.layout()
        A.draw("CFG.png")

    def print_block(self, block=None, name=None):
        """
        Prints the instructions of a block.
        """
        if block and name and block.name != name:
            raise Exception("You passed a name and a block, but the two don't correspond:\
block.name != name")
        if block and not name:
            print block
        elif name:
            print self.get_block(name)

    def remove_block(self, name):
        """
        Removes the block corresponding to the name and all its edges
        """
        removed = False
        for i,block in enumerate(self.blocks):
            if block.name == name:
                del self.blocks[i]
                removed = True
                break
        for i,edge in enumerate(self.edges):
            if name in edge:
                self.edges.remove(edge)
        return removed
    
    def get_out_edges(self, block=None, name=None):
        """
        Returns all (a list) edges that come out of the given block.
        You can pass the name of a block or the 
        """
        _out = []
        if block and name and block.name != name:
            raise Exception("You passed a name and a block, but the two don't correspond:\
block.name != name")
        else:
            for edge in self.edges:
                if (block and edge[0] == block.name) or (name and edge[0] == name):
                    _out.append(edge)
        return _out
        
    def get_in_edges(self, block=None, name=None):
        """
        Returns all (a list) edges that go into the given block.
        """
        _in = []
        if block and name and block.name != name:
            raise Exception("You passed a name and a block, but the two don't correspond:\
block.name != name")
        else:    
            for edge in self.edges:
                if (block and edge[1] == block.name) or (name and edge[1] == name):
                    _in.append(edge)
        return _in
    
    def get_blockname(self, block):
        """
        Returns the name of a given block
        """
        return block.name
        
    def get_block(self, name):
        """
        Given a name, the corresponding block object is returned.
        """
        for block in self.blocks:
            if block.name == name:
                return block
    
    def cfg_to_flat(self):
        """
        Convert Control Flow Graph to list of expression objects.
        """
        
        return sum((list(block) for block in self.blocks), [])

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('opt.txt', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    c = CFG(flat)
    return c
if __name__ == '__main__':
    #main()
    pass
