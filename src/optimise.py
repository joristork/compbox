#!/usr/bin/env python

#
# optimise.py
#

from optparse import OptionParser

from asmyacc import parser
from ir import Raw
from cfg import CFG
from block_optimise import AlgebraicTransformations as AT
from block_optimise import ConstantFold as CF



def split_frames(flat):
    """
    Split list of expression objects in 'frames'.
    
    """
    
    frames = [[]]
    for expr in flat:
        # A new frame starts with a .loc expression.
        if type(expr) == Raw and expr.expr[:4] == '.loc':
            frames.append([expr])
        else:
            frames[-1].append(expr)
    return frames



class Optimiser(object):
    """
    Main Optimiser.

    Tasks:
     1. convert source to IR;
     2. optimise IR;
     3. convert IR back to source.
     
    """
    
    def __init__(self, lines):
        """
        Convert expressions to IR.
        """
        
        # Parse assembly and store in flat.
        self.flat = []
        for line in lines:
            if not line.strip():
                # We skip empty lines. We could also tell yacc to put them in a Raw.
                continue
            self.flat.append(parser.parse(line))


    def optimise(self):
        """
        Optimise the IR.

        Procedure:
         1. split in frames
         2. convert frames to graphs
         3. optimise graphs
         4. convert graphs to (flat) frames
         5. concatenate frames to get optimised program.

        Store result in flat.
        
        """

        frames = split_frames(self.flat)
        graphs = [CFG(frame) for frame in frames]

        # work in progress: optimise graphs (block level)
        for graph in graphs:
            for block in graph.blocks:
                optimiser = AT(block)
                optimiser.optimise()
                cf_optimiser = CF(block)
                cf_optimiser.optimise()

        frames = [graph.cfg_to_flat() for graph in graphs]
        self.flat = sum(frames, [])

    
    def result(self):
        """
        Return optimised assembly.
        """
        
        return [str(expr)+'\n' for expr in self.flat]


def main():
    """ Parse command line args, init. optimiser and run optimisations. """

    usage = "usage: %prog [options] file"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dest", dest="filename",
                      help="save result in FILENAME")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    
    sourcefile = open(args[0], 'r')
    opt = Optimiser(sourcefile.readlines())
    sourcefile.close()
    
    opt.optimise()

    if options.filename:
        target_filename = options.filename
    else:
        target_filename = args[0] + '.opt'

    targetfile = open(target_filename, 'w')
    targetfile.writelines(opt.result())
    targetfile.close()

if __name__ == '__main__':
    main()

    
    
    
