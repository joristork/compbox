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
        self.expr = expr

    def __repr__(self):
        return 'Op(%r)' % self.expr


class Block(object):
    """
    Block acts as a node in the graph that Graph represents. Nodes represent a
    piece of assembly with a single entry point and a single exit point.

    Tasks:
     - give/change code lines;
     - give/change blocks pointing to this block;
     - give/change blocks that this block points to.

    """

    def __init__(self, lines, in_block):
        self.lines = [Op(line) for line in lines]
        self.in_block = in_block

    def __repr__(self):
        return 'Block(%r)' % self.lines


class Graph(object):
    """
    Intermediate representation (IR) of source code in the peephole Optimiser.

    The nodes of the graph are Block s.

    Tasks:
     - convert assembly to Graph;
     - convert graph to assembly;
     - give list of blocks.

    """
    
    def __init__(self, lines):
        self.blocks = [Block(lines, None),] # just an example; is wrong.

    def __repr__(self):
        return  'Graph(%r)' % self.blocks


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
    main()
