#!/usr/bin/env python

#
# optimise.py
#

from optparse import OptionParser
import logging

import parse_instr
import optimise_tree
import flat as flat_opt

from asmyacc import parser
from ir import Raw
from cfg import CFG
from dataflow import Dataflow
from liveness import Liveness

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
        self.stats = {'cp':0,'cf':0,'dc':0}
        self.logger = logging.getLogger('Optimiser')

        self.logger.info('parsing assembly')
        # Parse assembly and store in flat.
        self.flat = []
        for line in lines:
            if not line.strip():
                # We skip empty lines. We could also tell yacc to put them in a Raw.
                continue
            self.flat.append(parser.parse(line))
        self.flat = parse_instr.parse(self.flat)


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

        self.logger.info('optimising global control flow graph')
        
        cfg = CFG(self.flat)
        if self.verbosity > 2:
            cfg.cfg_to_diagram("allinstr_graph_before.png")    
        optimise_tree.optimise(cfg)
        if self.verbosity > 2:
            cfg.cfg_to_diagram("allinstr_graph_after.png")      
        self.flat = cfg.cfg_to_flat()
        
        self.logger.info('optimising flat (jumps and branches)')
        self.flat = flat_opt.optimise(self.flat)
        
        
         


        self.logger.info('splitting flat in frames')
        frames = split_frames(self.flat)
        self.logger.info('creating graph for each frame')
        graphs = [CFG(frame) for frame in frames]  
        
        self.logger.info('optimising blocks')    

        for graphnr, graph in enumerate(graphs):
            self.logger.info('graph %d of %d' % (graphnr + 1, len(graphs)))

            Dataflow(graph)
            l = Liveness(graph)

            #self.logger.info('Performing liveness optimalisation on graph')
            #change = True
            #while change:
            #    l.analyse()
            #    change = l.optimise()     
                        
            for blocknr, block in enumerate(graph.blocks):
            
                self.logger.debug('block %d of %d' % (blocknr + 1, len(graph.blocks)))
               
                cf_opt = b_opt.ConstantFold(block)
                cp_opt = b_opt.CopyPropagation(block)
                dc_opt = b_opt.DeadCode(block)

                done = False
                subopt_changes = False
                i = 0

                while (not done):
                    done = True
                    i += 1
                    self.logger.debug('pass '+str(i))

                    subopt_changes = cf_opt.optimise()
                    if subopt_changes:self.stats['cf'] += cf_opt.stats['cf']
                    done = done & (not subopt_changes)

                    subopt_changes = cp_opt.optimise()
                    if subopt_changes:self.stats['cp'] += cp_opt.stats['cp']
                    done = done & (not subopt_changes)
                    
                    #subopt_changes = dc_opt.optimise()
                    #if subopt_changes:self.stats['dc'] += dc_opt.stats['dc']
                    #done = done & (not subopt_changes)

        self.logger.info('basic-block peephole optimisations done:')
        self.logger.info('\t\tconstant folds: %d' % (self.stats['cf']))
        self.logger.info('\t\tcopy propagations: %d' % (self.stats['cp']))
        self.logger.info('\t\tdead code removes: %d' % (self.stats['dc']))
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
                      help="save result in FILENAME, overrides -e, --extension")
    parser.add_option("-v", "--verbosity", dest="verbosity",
            help="set verbosity (0: critical, 1: error, 2: warning, 3: info, 4: debug)")
    parser.add_option("-e", "--extension", dest="extension",
            help="save result in source filename + EXTENSION")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')

    if not options.verbosity:
        options.verbosity = 2

    if not options.extension:
        options.extension = '.opt'

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
        target_filename = args[0] + options.extension

    targetfile = open(target_filename, 'w')
    logging.info('writing optimised assembly to file')
    targetfile.writelines(opt.result())
    targetfile.close()

if __name__ == '__main__':
    main()

    
    
    
