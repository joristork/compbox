#!/usr/bin/env python

#
# optimise.py
#

import sys

# Option parsing module:
# from optparse import OptionParser

# Our own Optimiser modules:
# import modules

from asmyacc import parser

from ir import Raw
from cfg import CFG

def split_frames(flat):
    frames = []
    frames.append([])
    for expr in flat:
        if type(expr) == Raw and expr.expr[:4] == '.loc':
            frames.append([])
            frames[-1].append(expr)
        else:
            frames[-1].append(expr)
    return frames

class Optimiser(object):
    """
    Main Optimiser.

    Tasks
     - convert source to IR;
     - let Optimiser modules optimise the IR;
     - convert IR back to source.
    """
    
    def __init__(self, lines):
        #print 'Optimiser\nsource: %s' % lines

        self.flat = []
        for line in lines:
            if not line.strip():
                continue
            self.flat.append(parser.parse(line))


    def optimise(self):

        frames = split_frames(self.flat)

        graphs = [CFG(frame) for frame in frames]

        # optimise graphs

        frames = [graph.cfg_to_flat() for graph in graphs]

        self.flat = sum(frames, [])
    

def main():
    """ Parse command line args, init. optimiser and run optimisations. """

    # Use plain sys.argv[1] for now. optparse is for later.
    if len(sys.argv) != 2:
        print "argument expected"
        return
    sourcefile = open(sys.argv[1], 'r')
    opt = Optimiser(sourcefile.readlines())
    sourcefile.close()
    
    opt.optimise()

    targetfile = open(sys.argv[1] + '.opt', 'w')
    targetfile.writelines([str(expr)+'\n' for expr in opt.flat])
    targetfile.close()

if __name__ == '__main__':
    main()

    
    
    
