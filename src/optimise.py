#!/usr/bin/env python

#
# optimise.py
#

from optparse import OptionParser
import logging

from asmyacc import parser
from ir import Raw
from cfg import CFG
import block_optimise as b_opt



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
    
    def __init__(self, lines, verbosity = 0):
        """
        Convert expressions to IR.
        """
        
        self.verbosity = verbosity
        self.stats = {}
        self.logger = logging.getLogger('Optimiser')

        self.logger.info('parsing assembly')
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

        self.logger.info('splitting flat in frames')
        frames = split_frames(self.flat)
        self.logger.info('creating graph for each frame')
        graphs = [CFG(frame) for frame in frames]

        for graph in graphs:
            for block in graph.blocks:

                cf_opt = b_opt.ConstantFold(block)
                cp_opt = b_opt.CopyPropagation(block)
                dc_opt = b_opt.DeadCode(block)

                done = False
                no_subopt_changes = True
                i = 0

                while (not done):
                    done = True
                    i += 1
                    self.logger.info('peephole optimising, pass '+str(i))

                    no_subopt_changes = cf_opt.optimise()
                    done = done & no_subopt_changes

                    no_subopt_changes = cp_opt.optimise()
                    done = done & no_subopt_changes
                    
                    no_subopt_changes = dc_opt.optimise()
                    done = done & no_subopt_changes

        self.logger.info('joining graphs to frames')
        frames = [graph.cfg_to_flat() for graph in graphs]
        self.logger.info('joining frames to flat')
        self.flat = sum(frames, [])

    
    def result(self):
        """
        Return optimised assembly.
        """
       
        self.logger.info('generating assembly')
        return [str(expr)+'\n' for expr in self.flat]




def main():
    """ Parse command line args, init. optimiser and run optimisations. """


    usage = "usage: %prog [options] file"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dest", dest="filename",
                      help="save result in FILENAME")
    parser.add_option("-v", "--verbosity", dest="verbosity",
            help="set verbosity (0: critical, 1: error, 2: warning, 3: info, 4: debug)")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')

    if not options.verbosity:
        options.verbosity = 2

    logging_levels = {0: logging.CRITICAL,
                      1: logging.ERROR,
                      2: logging.WARNING,
                      3: logging.INFO,
                      4: logging.DEBUG}
    
    logging.basicConfig(format='%(asctime)s %(levelname)-7s %(name)-14s %(message)s',
                        level=4,
                        filename='log',
                        filemode='w'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging_levels[int(options.verbosity)])
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-7s %(name)-14s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


    logger = logging.getLogger('main')
    logger.info('opening sourcefile')
    try:
        sourcefile = open(args[0], 'r')
    except IOError:
        print('error: file not found: %s' % args[0])
        exit(1)
    opt = Optimiser(sourcefile.readlines(), options.verbosity)
    sourcefile.close()
    logger.info('sourcefile closed')

    opt.optimise()

    if options.filename:
        target_filename = options.filename
    else:
        target_filename = args[0] + '.opt'

    targetfile = open(target_filename, 'w')
    logging.info('writing optimised assembly to file')
    targetfile.writelines(opt.result())
    targetfile.close()

if __name__ == '__main__':
    main()

    
    
    
