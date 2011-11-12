#!/usr/bin/env python

#
# optimise.py
#

import sys

# Option parsing module:
# from optparse import OptionParser

# Our own Optimiser modules:
# import modules

class Op(object):
    """
    Op represents one assembly expression.

    This expression has an instruction, arguments and a line number.

    Tasks:
     - give instruction type (control, load/store, integer, floating-point, miscellaneous);
     - give arguments;
     - convert expression to Op instance;
     - convert Op instance back to expression.

    """
    
    def __init__(self, expr):
        self.previous_line = None
        self.next_line = None
        self.original_line_nr = None
        self.expr = expr
        self.destinations = []
        self.leader = False
        self.type = None
        self.args = []

    def __repr__(self):
        return 'Op(%r)' % self.expr

    def parse(self, expr):
        pattern = re.compile('[\s,]+')
        expr_elements = pattern.split(expr.lstrip(' ,'))
        self.type = expr_elements[0]
        if expr_elements[0].startswith("B"):
            offset = int(expr_elements[-1])
            self.destinations.append(offset + self.original_line_nr)


class Block(object):
    """
    Block acts as a node in the graph that Graph represents. Nodes represent a
    piece of assembly with a single entry point and a single exit point.

    Tasks:
     - give/change code lines;
     - give/change blocks pointing to this block;
     - give/change blocks that this block points to.

    """

    block_id = -1

    def __init__(self, block_id=None, ops=None, out=None):
        if not block_id:
            Block.block_id += 1
            self.block_id = Block.block_id
        elif block_id == 'entry':
            self.block_id='entry'
            Block.block_id = -1
        elif block_id == 'exit':
            self.block_id = 'exit'
        else:
            self.block_id = block_id
            Block.block_id = block_id
        self.ops = []
        self.next = None
        self.jump = None

    def __str__(self):
        next_block_id = self.next.block_id if self.next else None
        jump_block_id = self.jump.block_id if self.jump else None
        return 'Block(%s, %s, next=%s, jump=%s)' % (self.block_id, self.ops, next_block_id, jump_block_id)
        
    def __repr__(self):
        return '<Block id=%s>' % str(self.block_id)

    def append(self, op):
        self.ops.append(op)
        op.block = self



class Graph(object):
    """
    Intermediate representation (IR) of source code in the peephole Optimiser.

    The nodes of the graph are Block s.

    Tasks:
     - convert assembly to Graph;
     - convert graph to assembly;
     - give list of blocks.

    """

    entry_block = Block('entry')
    exit_block = Block('exit')

    def __init__(self, lines, op_class=Op):

        self.blocks = []
        self.OpClass = op_class # we can change this class for testing purposes
        
        self.assembly_to_graph(lines)
        
        

    def assembly_to_graph(self, lines):
        ops  = []
        leaders = []
        jumps = {}
        nexts = {}

        if not lines:
            return
          
        # create ops
        for line in lines:
            ops.append(self.OpClass(line))

        # find leaders and jump destinations
        for index, op in enumerate(ops): 
            if op.type == 'control':
                jump_target_index = op.get_jump_target_index(index)
                if jump_target_index < len(ops):
                    leaders.append(ops[op.get_jump_target_index(index)])
                    jumps[op] = ops[jump_target_index]
                else:
                    jumps[op] = None # (jumps to exit block)
                if index+1 < len(ops):
                    leaders.append(ops[index + 1])

            if index+1 < len(ops):
                nexts[op] = ops[index+1] # TODO: if jump is uncoditional, there is no next.
            else:
                nexts[op] = None # (next is exit block)            
                

        # create blocks according to leaders
        block = Block()
        block.append(ops[0])
        self.blocks.append(block)
        for op in ops[1:]:
            if op in leaders:
                block = Block()
                self.blocks.append(block)
            block.append(op)

        # set edges for jumps between blocks and set edges
        # between consecutive blocks
        for block in self.blocks:
            last_op = block.ops[-1]

            next_op = nexts[last_op]
            if next_op:
                block.next = next_op.block
            else:
                block.next = self.exit_block

            if last_op.type == 'control':
                target_op = jumps[last_op]
                if target_op:
                    block.jump = target_op.block
                else:
                    block.jump = self.exit_block
            else:
                block.jump = None
                    

    def __str__(self):
        return  'Graph(%s)' % ', '.join([str(b) for b in self.blocks])


class Optimiser(object):
    """
    Main Optimiser.

    Tasks
     - convert source to IR;
     - let Optimiser modules optimise the IR;
     - convert IR back to source.

    """
    
    def __init__(self, lines):
        self.graph = Graph(lines)
        print 'Optimiser\nsource: %s' % lines
        print 'graph: %s' % self.graph


def main():
    """ Parse command line args, init. optimiser and run optimisations. """

    # Use plain sys.argv[1] for now. optparse is for later.
    if len(sys.argv) != 2:
        print "argument expected"
        return
    sourcefile = open(sys.argv[1], 'r')
    opt = Optimiser(sourcefile.readlines())
    sourcefile.close()


if __name__ == '__main__':
    #main()
    import test_graph
    test_graph.test()
    
    
