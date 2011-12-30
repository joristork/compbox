""" 
File:         block_optimise.py
Course:       Compilerbouw 2011
Author:       Joris Stork

The block optimiser module

Description:
    blah

"""


from cfg import BasicBlock
from ir import Instr
import math
from peephole import Peephole, Peeper
from uic import copy_prop_targets

class BlockOptimiser(object):
    """ Parent class for the various block optimisations.  """


    def __init__(self, block = None, peephole_size = None):
        """ By default the peephole size is that of the basic block """

        self.verbosity = 0
        self.block = block
        if not peephole_size:
            self.p_size = len(block)
        else:
            self.p_size = peephole_size


    def set_block(self, block):
        """ Optimiser can be re-assigned to a new block  """
        
        self.block = block


    def set_peephole_size(self, size):
        """ Optimiser can be tweaked with a new peephole size. """

        self.p_size = size


    def rename_temp_vars(self):
        """ Renames temporary variables until bb is in normal form."""
        pass


    def find_constants(self, before = 0):
        """ 
        compiles a dict of (register,constant) pairs, with the constant
        corresponding to the last value in the given register before the
        ``before'' register 
        
        """
        consts = {}
        for ins in self.peephole[0:before]:
            if isinstance(ins,Instr):
                if ins.instr == 'li':
                    consts[ins.args[0]] = ins.args[1]
        return consts


    def suboptimisation(self):
        """ Defined in subclass  """

        pass


    def optimise(self):
        """ If block assigned, runs sub-optimisation until exhausted. """

        if not self.block: 
            """ raise an exception here """
            return
        peeper = Peeper(self.block, self.p_size)
        for peephole in peeper:
            self.peephole = peephole
            while self.suboptimisation():
                pass



class CommonSubexpressions(BlockOptimiser):
    """ Block optimisation: duplicate subexpressions -> variables"""

    def suboptimisation(self):
        """ If duplicate subexpression found within peephole,  """

        optimised = False

        return optimised



class ConstantFold(BlockOptimiser):
    """ replaces arithmetic expression with only constants, with value """


    def addu(self, i, ins, opt, consts):
        """ 
        replaces addu instruction with value. Though not guaranteed to replicate
        unsigned behaviour, should be ok for benchmarks (c.f. report)
        
        """    
        optimised = opt
        if ins.instr == 'addu':
            if (ins.args[1] in consts) & (ins.args[2] in consts):
                newins = Instr('li',[ins.args[0],consts[ins.args[1]]+consts[ins.args[2]]])
                self.peephole[i] = newins
                consts[newins.args[0]] = newins.args[1]
                if self.verbosity == 2 : print 'did a constant fold\n'
                optimised = True
        return optimised


    def suboptimisation(self):
        """ if 2+ compile time constants, tries constant folding """
        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                consts = self.find_constants(i)
                if len(consts) > 1:
                    optimised = self.addu(i, ins, optimised, consts)
        return optimised



class AlgebraicTransformations(BlockOptimiser):
    """ contains various algebraic transformation optimisations  """
    # Need to look for values of variables

    def divd_to_sra(self, i, ins, opt, consts):
        """ shift-right arithmetic is faster than division...  """
        optimised = opt
        if ins.instr == 'div.d':
            if (ins.args[1] in consts) & (ins.args[2] in consts):
                n = math.log(consts[ins.args[2]], 2)
                if n % 1 == 0:
                    newins = Instr('sra', [ins.args[0], consts[ins.args[1]], n])
                    self.peephole[i] = newins
                    if self.verbosity == 2 : print 'changed a div to an sra'
                    optimised = True
        return optimised


    def suboptimisation(self):
        """   """
        
        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                consts = self.find_constants(i)
                optimised = self.divd_to_sra(i, ins, optimised, consts)
                #TODO: any other algebraic opts? (sla not available)
        return optimised



class CopyPropagation(BlockOptimiser):
    """ after copy, propagate original variable where copy unaltered """

    def propagate_from_move(self, i, ins, opt):
        """ if a move, substitutes subsequent uses of unaltered copy value """
        optimised = opt
        if ins.instr == 'move': 
            if self.verbosity == 1 : print 'found a move\n'
            safe = True
            orig = ins.args[1]
            if self.verbosity == 1 : print 'orig: ',orig,'\n'
            copy = ins.args[0] # nb: move not explicity defined for simplescalar
            if self.verbosity == 1 : print 'copy: ',copy,'\n'
            for i2, ins2 in enumerate(self.peephole[i+1:len(self.peephole)]):
                valid_target = False
                if ins2.instr in copy_prop_targets:
                    valid_target = True
                # ripe for refining: copy value might be used not written to
                if self.verbosity == 1 : print 'looking for copy in: ',str(ins2),'\n'
                if copy not in ins2.args:
                    continue
                elif (copy in ins2.args[0]) & valid_target:
                    if self.verbosity == 1 : print 'copy possibly assigned to\n'
                    if safe & (ins2.args.count(copy) > 1):
                        first = ins2.args.index(copy)
                        second = ins2.args[first+1:len(ins2.args)].index(copy)
                        second = second + first + 1
                        ins2.args[second] = orig
                        self.peephole[i+1+i2] = ins2
                        if self.verbosity == 2 : print 'copy propagation: substituted original reference for pointer.\n'
                        if self.verbosity == 1 : print 'still a safe propagation target: substituted\n'
                    safe = False
                elif valid_target & safe:
                    if self.verbosity == 1 : print 'safe propagation target: substituted\n'
                    ins2.args[ins2.args.index(copy)] = orig
                    self.peephole[i+1+i2] = ins2
                    optimised = True
                    if self.verbosity == 2 : print 'copy propagation: substituted original reference for pointer.\n'
                else:
                    if self.verbosity == 1 : print 'unknown situation: assume danger\n'
                    safe = False
        return optimised
                            

    def suboptimisation(self):
        """ 
        finds copies; then: if unaltered copy used later, substitute with
        original; else ignore
        
        """

        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                optimised = self.propagate_from_move(i, ins, optimised)
        return optimised



class DeadCode(BlockOptimiser):
    """   """

    def suboptimisation(self):
        """   """
        
        optimised = False

        return optimised



class TempVarRename(BlockOptimiser):
    """   """

    def suboptimisation(self):
        """   """

        optimised = False

        return optimised



class ExchangeIndependentStatements(BlockOptimiser):
    """   """

    def suboptimisation(self):
        """   """

        optimised = False

        return optimised



class MachineDependentTransformations(BlockOptimiser):
    """   """

    def suboptimisation(self):
        """   """

        optimised = False

        return optimised
