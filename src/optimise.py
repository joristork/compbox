#!/usr/bin/env python

#
# optimise.py
#

import sys
from optparse import OptionParser
import logging

from asmyacc import parser
from ir import Raw
from cfg import CFG

from dataflow import Dataflow
from liveness import Liveness
import block_optimise as b_opt
import parse_instr
import optimise_tree
import flat as flat_opt



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
    
    def __init__(self, lines, verbosity = 0, enabled_optimisations = None):
        """
        Convert expressions to IR.
        """
        
        self.verbosity = verbosity
        self.logger = logging.getLogger('Optimiser')
        if enabled_optimisations == None:
            self.enabled_optimisations = 'abcdefghijkl'
        else:
            self.enabled_optimisations = enabled_optimisations

        self.stats = {'cp':0, 'cf':0, 'dc':0}

        self.logger.info('parsing assembly')
        # Parse assembly and store in flat.
        self.flat = []
        for line in lines:
            if not line.strip():
                # We skip empty lines. We could also tell yacc to put them in a Raw.
                # TODO: skippet yacc dit niet sowieso?
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


        # top loop
        
        flat_orig = None
        top_loop_counter = 0
        while True:
            if flat_orig == self.flat:
                self.logger.info('optimisation is stable')
                break
            if top_loop_counter == 10000:
                self.logger.warning('top loop limit reached (10000 iterations)')
                break
            flat_orig = self.flat[:]
            top_loop_counter += 1
            self.logger.info('top pass %s' % str(top_loop_counter))           

            # a.
            if 'a' in self.enabled_optimisations:
                self.logger.info('optimising global control flow graph')
            
                cfg = CFG(self.flat)
                #if self.verbosity > 2:
                #    cfg.cfg_to_diagram("allinstr_graph_before.png")    
        
                optimise_tree.optimise(cfg)
                #if self.verbosity > 2:
                #    cfg.cfg_to_diagram("allinstr_graph_after.png")      
                self.flat = cfg.cfg_to_flat()
              
            # b. jump optimisations 
            if 'b' in self.enabled_optimisations:
                self.logger.info('optimising flat (jumps and branches)')
                self.flat = flat_opt.optimise(self.flat)
            

            self.logger.info('splitting flat in frames')
            frames = split_frames(self.flat)
            self.logger.info('creating graph for each frame')
            graphs = [CFG(frame) for frame in frames]  
            
            
            self.logger.info('optimising blocks')    

            for graphnr, graph in enumerate(graphs):
                self.logger.info('graph %d of %d' % (graphnr + 1, len(graphs)))

                #Dataflow(graph)
                if 'f' in self.enabled_optimisations:
                    l = Liveness(graph,self.verbosity)
                    self.logger.info('Performing liveness optimalisation on graph')
                    change = True
                    while change:
                        l.analyse()
                        change = l.optimise()   
                            
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
                        self.logger.debug('\t pass '+str(i))
                   
                        # c. constant folding
                        if 'c' in self.enabled_optimisations:
                            subopt_changes = cf_opt.optimise()
                            if subopt_changes: self.stats['cf'] += cf_opt.stats['cf']
                            done = done & (not subopt_changes)

                        # d. copy propagation
                        if 'd' in self.enabled_optimisations:
                            subopt_changes = cp_opt.optimise()
                            if subopt_changes:self.stats['cp'] += cp_opt.stats['cp']
                            done = done & (not subopt_changes)
                        
                        # e. dead code removal
                        if 'e' in self.enabled_optimisations:
                            subopt_changes = dc_opt.optimise()
                            if subopt_changes:self.stats['dc'] += dc_opt.stats['dc']
                            done = done & (not subopt_changes)

            self.logger.info('basic-block peephole optimisations done:')
            self.logger.info('\t constant folds: %d' % (self.stats['cf']))
            self.logger.info('\t copy propagations: %d' % (self.stats['cp']))
            self.logger.info('\t dead code removes: %d' % (self.stats['dc']))

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
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False,
            help="no optimisations, only parsing and code generation. -o '' is equivalent.")
    parser.add_option("-o", "--optimisations", dest="optimisations", default=None,
            help="enable specific optimisations, default is all")

    parser.add_option("-m", "--meld", action="store_true", dest="meld", default=False,
            help="after optimising open meld to show diff")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error('incorrect number of arguments')

    if not options.verbosity:
        options.verbosity = 2

    if not options.extension:
        options.extension = '.opt'

    if options.test:
        options.optimisations = ''
 

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
    logger.info(' '.join(sys.argv[1:]))
    logger.info('opening sourcefile')
    try:
        sourcefile = open(args[0], 'r')
    except IOError:
        print('error: file not found: %s' % args[0])
        exit(1)
    opt = Optimiser(sourcefile.readlines(), options.verbosity, options.optimisations)
    sourcefile.close()
    logger.info('sourcefile closed')

    opt.optimise()

    if options.filename:
        target_filename = options.filename
    else:
        target_filename = args[0] + options.extension

    targetfile = open(target_filename, 'w')
    logger.info('writing optimised assembly to file')
    targetfile.writelines(opt.result())
    targetfile.close()

    if options.meld:
        import subprocess
        print args[0], target_filename
        subprocess.call(['meld', args[0], target_filename], shell=False)

if __name__ == '__main__':
    main()

    
    
    
