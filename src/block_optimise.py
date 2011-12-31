""" 
File:         block_optimise.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam


Description:
    Defines the various subclasses of block optimiser. Currently implemented:
        ConstantFold
        DeadCode
        CopyPropagation

"""


from cfg import BasicBlock
import ir
from ir import Instr
import math
from peephole import Peephole, Peeper
from uic import copy_prop_targets, copy_prop_unsafe, assign_to
import logging


class BlockOptimiser(object):
    """ Parent class for the various block optimisations.  """


    def __init__(self, block = None, peephole_size = None):
        """ By default the peephole size is that of the basic block """

        self.block = block
        self.stats = {'dc':0,'cp':0,'cf':0}
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
        we can improve this function by keeping track of constants, e.g. after
        moves.
        
        """
        consts = {}
        for ins in self.peephole[0:before]:
            if isinstance(ins,Instr):
                if ins.instr == 'li':
                    consts[ins.args[0].expr] = ins.args[1]
        return consts


    def suboptimisation(self):
        """ Defined in subclass  """

        pass


    def optimise(self):
        """ If block assigned, runs sub-optimisation until exhausted. """

        changed = False
        if not self.block: 
            """ raise an exception here """
            return changed
        peeper = Peeper(self.block, self.p_size)
        optimised = False
        for peephole in peeper:
            self.peephole = peephole
            optimised = True
            while optimised:
                optimised = self.suboptimisation()
                changed = changed | optimised
        return changed



class ConstantFold(BlockOptimiser):
    """ Replaces arithmetic expression with only constants, with value """


    def addu(self, i, ins, opt, consts):
        """ 
        Replaces addu instruction with value. Though not guaranteed to replicate
        unsigned behaviour, should be ok for benchmarks (c.f. report)
        Note: We take into account that addu's might include compile-time
        immediate values, since we encountered that in the benchmark code. Addu
        seems to incorporate addiu functionality since no addiu's were found in
        the benchmark code.
        
        """    
        optimised = opt
        if ins.instr == 'addu':

            arg1_is_reg = isinstance(ins.args[1],ir.Register)
            arg2_is_reg = isinstance(ins.args[2],ir.Register)
            none_reg = (not arg1_is_reg) & (not arg2_is_reg)
            arg1_known_reg = False
            arg2_known_reg = False
            if arg1_is_reg:
                arg1_known_reg = (ins.args[1].expr in consts)
            if arg2_is_reg:
                arg2_known_reg = (ins.args[2].expr in consts)
            both_known_regs = arg1_known_reg & arg2_known_reg
            c1 = None
            c2 = None
            optimised_this_time = True

            if both_known_regs:
                c1 = consts[ins.args[1].expr]
                c2 = consts[ins.args[2].expr]
            elif none_reg:
                c1 = ins.args[1]
                c2 = ins.args[2]
            elif arg1_known_reg & (not arg2_is_reg):
                c1 = consts[ins.args[1].expr]
                c2 = ins.args[2]
            elif arg2_known_reg & (not arg1_is_reg):
                c1 = ins.args[1]
                c2 = consts[ins.args[2].expr]
            else:
                optimised_this_time = False

            if optimised_this_time:
                if isinstance(c1,str):
                    c1 = int(c1,0)
                if isinstance(c2,str):
                    c2 = int(c2,0)
                fold = c1 + c2 
                self.logger.debug(' being replaced... '+str(self.peephole[i]))
                self.peephole[i] = Instr('li',[ins.args[0], hex(fold)])
                self.logger.debug('new instruction: '+str(self.peephole[i]))
                consts[self.peephole[i].args[0].expr] = self.peephole[i].args[1]
                optimised = True
                self.logger.debug('constant folded')
                self.stats['cf'] += 1
        return optimised


    def suboptimisation(self):
        """ if 2+ compile time constants, tries constant folding """
        self.logger = logging.getLogger('ConstantFold')
        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                consts = self.find_constants(i)
                if len(consts) > 1:
                    optimised = self.addu(i, ins, optimised, consts)
        return optimised



class CopyPropagation(BlockOptimiser):
    """ after copy, propagate original variable where copy unaltered """

    def propagate_from_move(self, i, ins, opt):
        """ if a move, substitutes subsequent uses of unaltered copy value """
        optimised = opt
        if ins.instr == 'move': 
            orig = ins.args[1]
            copy = ins.args[0] # nb: move not explicity defined for simplescalar
            for i2, ins2 in enumerate(self.peephole[i+1:len(self.peephole)]):
                if isinstance(ins2,Instr):
                    args = []
                    for arg in ins2.args:
                        if isinstance(arg,str) | isinstance(arg,int) :
                            args.append(arg)
                        else:
                            args.append(arg.expr)
                if not isinstance(ins2, Instr):
                    continue
                elif str(ins2.instr) not in copy_prop_targets:
                    unsafe = str(ins2.instr) in copy_prop_unsafe
                    if unsafe & ((copy.expr in args) | (orig.expr in args)):
                        return optimised
                    else: continue
                elif copy.expr in args:
                    argsize = len(ins2.args)
                    if copy.expr in args[1:argsize]:
                        one = args[1:argsize].index(copy.expr) + 1
                        self.logger.debug(' being replaced... '+str(self.peephole[i+1+i2]))
                        ins2.args[one] = orig
                        if args[1:argsize].count(copy.expr) == 2:
                            two=args[one+1:argsize].index(copy.expr)+one+1
                            ins2.args[two] = orig
                        self.peephole[i+1+i2] = ins2
                        self.logger.debug('new instruction: '+str(self.peephole[i+1+i2]))
                        optimised = True
                        self.logger.debug('copy propagated')
                        self.stats['cp'] += 1

                    if (copy.expr==args[0]) | (orig.expr in args[0]):
                        return optimised
                else:
                    continue
        return optimised
                            

    def suboptimisation(self):
        """ 
        finds copies; then: if unaltered copy used later, substitute with
        original; else ignore
        
        """

        self.logger = logging.getLogger('CopyPropagation')
        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                optimised = self.propagate_from_move(i, ins, optimised)
        return optimised



class DeadCode(BlockOptimiser):
    """ 
    Finds and removes instructions that assign a value that is then never used.  
    
    """


    def subscan(self, i, ins, opt, cand_reg_index):
        """ 
        Searches subsequent instructions, and: stops if candidate register is
        used; or removes the candidate instruction if register is overwritten.
        Note: the only instruction object without an args attribute is the nop
        instruction. Such instructions are ignored.

        """
        optimised = opt
        for i2, ins2 in enumerate(self.peephole[i+1:len(self.peephole)]):
            candidate_reg = ins.args[cand_reg_index]
            ins2_is_instruction = isinstance(ins,Instr)
            args = []
            if ins2_is_instruction:
                try:
                    for arg in ins2.args:
                        if isinstance(arg,str) | isinstance(arg,int) :
                            args.append(arg)
                        else:
                            args.append(arg.expr)
                except AttributeError:
                    continue
            if not ins2_is_instruction:
                continue
            elif candidate_reg.expr not in args:
                continue
            elif str(ins2.instr) in assign_to:
                assigned_to_index = assign_to[str(ins2.instr)]
                pre_args = args[0:assigned_to_index]
                post_args = args[assigned_to_index+1:len(args)]
                if candidate_reg.expr in pre_args+post_args:
                    return optimised
                else: 
                    self.logger.debug(' being removed... '+str(self.peephole[i]))
                    del self.peephole[i]
                    optimised = True
                    self.logger.debug('instruction removed')
                    self.stats['dc'] += 1
                    return optimised
            else: return optimised
        return optimised


    def suboptimisation(self):
        """   """
        
        optimised = False
        self.logger = logging.getLogger('DeadCode')
        candidate = None
        for i, ins in enumerate(self.peephole):
            if not isinstance(ins,Instr):
                continue
            elif str(ins.instr) in assign_to:
                cand_reg_index = assign_to[str(ins.instr)]
                optimised = self.subscan(i, ins, optimised, cand_reg_index)
        return optimised
