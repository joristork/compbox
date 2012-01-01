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
        self.genset = {}
        self.killset = {}
        self.inset = {}
        self.outset = {}
        
        self.killown = {}
        self.reach = {}
        self.liveout = []
        self.livein = []
        self.live_in_node = []
        self.live_in_node_reg = []
        
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

    def print_block(self):
        print "\nBlockname: ", self.name
        for ins in self.instructions:
            print ins        
    


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


        
    def load_flat(self, flat_ir):
        """
        Load list of expression objects in Control Flow Graph.
        """
        j = 0
        self.blocks.append(BasicBlock(name=str(j)))
        j += 1
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
                    and len(self.blocks) > 0):
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

    def cfg_to_diagram(self, name="CFG.png"):
        """
        Generates a diagram using the edges that were found when load_flat
        was executed. The result is saved in a png image file.
        """
        import pygraphviz as pgv
        A = pgv.AGraph(directed=True)
        for edge in self.edges: 
            A.add_edge(edge[0], edge[1])
        for block in self.blocks:
            if len(self.get_out_edges(block)) + len(self.get_in_edges(block)) == 0:
                A.add_node(block.name)
        A.layout()
        A.draw(name)

    def print_cfg(self):
        """
        Prints the name of each block, its instructions and its edges.

        NOTE: This function is not to be used to create assembly output.
        """
        for block in self.blocks:
            block.print_block()
            print "Edges: (out)", self.get_out_edges(block),\
            " (in)", self.get_out_edges(block)

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

        rm = []
        for edge in self.edges:
            if name == edge[0] or name == edge[1]:
                rm.append(edge)
        for r in rm:
            self.edges.remove(r)
        return removed
    
    def get_out_edges(self, block):
        """
        Returns all (a list) edges that come out of the given block.
        You can pass the name of a block or the 
        """
        _out = []
        if type(block) == BasicBlock:
            block = block.name
        for edge in self.edges:
            if (edge[0] == block):
                _out.append(edge)
        return _out
        
    def get_in_edges(self, block):
        """
        Returns all (a list) edges that go into the given block.
        """
        _in = []
        if type(block) == BasicBlock:
            block = block.name
        for edge in self.edges:
            if (edge[1] == block):
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
        return None
    
    def cfg_to_flat(self):
        """
        Convert Control Flow Graph to list of expression objects.
        """
        
        return sum((list(block) for block in self.blocks), [])

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/pi.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    c = CFG(flat)
    return c
if __name__ == '__main__':
    main()
    pass
