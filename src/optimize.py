#!/usr/bin/env python

#
# optimize.py
#

import sys

# Option parsing module:
# from optparse import OptionParser

# Our own optimizer modules:
# import modules

class Block(object):
    """
    Block acts as a node in the graph that Graph represents. Nodes represent a
    piece of assembly with a single entry point and a single exit point.

    Tasks:
     - give/change code lines;
     - give/change blocks pointing to this block;
     - give/change blocks that this block points to.
    """

    pass

class Graph(object):
    """
    Intermediate representation (IR) of source code in the peephole optimizer.

    The nodes of the graph are Block s.

    Tasks:
     - convert assembly to Graph;
     - convert graph to assembly;
     - give list of blocks.
    """
    
    pass

class Optimizer(object):
    """
    Main optimizer.

    Tasks
     - convert source to IR;
     - let optimizer modules optimize the IR;
     - convert IR back to source.
    """
    
    pass

def main():
    """
    Parse command line options, initiliaze Optimizer and run optimizations.
    """

if __name__ == '__main__':
    main()
