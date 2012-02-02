""" 
File:         block_optimise.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam


Description:
    Defines the various subclasses of block optimiser. 
    A block optimiser carries out optimisations through a Peephole object on
    BasicBlock objects (cfg.py), which represent basic blocks in the source
    code.
    
    The folllowing types of block optimisers are currently implemented:
        ConstantFold
        DeadCode
        CopyPropagation
    
    Other potential bb-optimisations to be found in block_optimise_lab.py

"""


from cfg import BasicBlock
import re
import ir
from ir import Instr
import math
from peephole import Peephole, Peeper
from uic import copy_prop_targets, copy_prop_unsafe, assign_to
import logging
from urc import j_thirty_one_regs, jal_regs


class BlockOptimiser(object):
    """ parent class for the various block optimisations """


    def __init__(self, block = None, peephole_size = None):
        """ by default the peephole size is that of the basic block """

        self.block = block
        self.stats = {'dc':0,'cp':0,'cf':0}

        if not peephole_size:
            self.p_size = len(block)
        else:
            self.p_size = peephole_size


    def set_block(self, block):
        """ re-assigns a new block to the optimiser """

        self.block = block


    def set_peephole_size(self, size):
        """ changes optimiser's peephole size setting """

        self.p_size = size


    def reg_indexes_in(self, subject, args):
        """ returns indexes of occurences of subject in args """

        indexes = []
        
        for i, arg in enumerate(args):
            if isinstance(arg, str):
                m = re.search('\$\w*', arg)
                if m:
                    arg_reg = m.group(0)
                else: continue
                if (arg_reg == subject):
                    indexes.append(i)
        
        return indexes


    def reg_in(self, subject, args):
        """ returns true if the string is a substring of one of args[i] """

        return (len(self.reg_indexes_in(subject, args)) > 0)

    
    def replace_reg(self, subject, arg):
        """ replaces register in arg with subject register """

        return ir.Register(re.sub('\$\w*', str(subject), str(arg)))


    def find_constants(self, before = 0):
        """ 
        compiles a dict of (register:constant) pairs, with the constant
        corresponding to the last value in the given register prior to the
        peephole[before] instruction
        
        """

        consts = {}

        for ins in self.peephole[0:before]:
            if isinstance(ins,Instr):
                if ins.instr == 'li':
                    consts[ins.args[0].expr] = ins.args[1]

        return consts


    def suboptimisation(self):
        """ defined in relevant optimisation subclass """

        pass


    def optimise(self):
        """ if block is present: runs sub-optimisation until no changes left """

        changed = False

        if not self.block: 
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



class CopyPropagation(BlockOptimiser):
    """ after copy, propagate original variable where copy unaltered """

    def propagate_from_move(self, i, ins, opt):
        """ 
        triggered by a move instruction; ignores non-instructions and
        instructions not containing the relevant registers; substitutes
        subsequent uses of unaltered copied-to (copy) register with the original
        (orig) register, until it finds an unsafe instruction with the orig or
        copy register, or until the orig or copy register are altered
        (substitution can still be done in the altering instruction) 
        
        """

        optimised = opt

        if ins.instr == 'move': 
            orig = ins.args[1]
            copy = ins.args[0] # nb: move not explicity defined for simplescalar
            
            for i2, ins2 in enumerate(self.peephole[i+1:len(self.peephole)]):

                if not isinstance(ins2,Instr):
                    continue

                args = []
                for arg in ins2.args:
                    if isinstance(arg,str) | isinstance(arg,int) :
                        args.append(arg)
                    else:
                        args.append(arg.expr)

                copy_in_args = self.reg_in(copy.expr, args)
                orig_in_args = self.reg_in(orig.expr, args)
                ins2_in_cp_targets = str(ins2.instr) in copy_prop_targets
                ins2_in_assignments = str(ins2.instr) in assign_to
                assigns_to = None

                if (ins2 in copy_prop_unsafe) & (copy_in_args | orig_in_args):
                    return optimised

                if (not ins2_in_cp_targets) & (not ins2_in_assignments):
                    continue
                elif not (copy_in_args | orig_in_args):
                    continue

                elif ins2_in_cp_targets:
                    
                    if ins2_in_assignments:
                        assigns_to = assign_to[str(ins2.instr)]
                        wrote_copy = self.reg_in(copy.expr,[args[assigns_to]])
                        wrote_orig = self.reg_in(orig.expr,[args[assigns_to]])
                        if copy_in_args:
                            for k in self.reg_indexes_in(copy.expr, args):
                                if not (k == assigns_to):
                                    msg = 'editing: '+str(self.peephole[i+1+i2])
                                    self.logger.debug(msg)
                                    old = ins2.args[k]
                                    ins2.args[k] = self.replace_reg(orig, old)
                                    optimised = True
                            if optimised:
                                self.peephole[i+1+i2] = ins2
                                msg = 'edited to: '+str(self.peephole[i+1+i2])
                                self.logger.debug(msg)
                                self.stats['cp'] += 1
                        if wrote_copy | wrote_orig:
                            return optimised

                    elif copy_in_args:
                        for k in self.reg_indexes_in(copy.expr, args):
                            msg = 'editing: '+str(self.peephole[i+1+i2])
                            self.logger.debug(msg)
                            old = ins2.args[k]
                            ins2.args[k] = self.replace_reg(orig, old)
                            optimised = True
                        self.peephole[i+1+i2] = ins2
                        msg = 'edited to: '+str(self.peephole[i+1+i2])
                        self.logger.debug(msg)
                        self.stats['cp'] += 1

                elif ins2_in_assignments:
                    assigns_to = assign_to[str(ins2.instr)]
                    wrote_copy = self.reg_in(copy.expr,[args[assigns_to]])
                    wrote_orig = self.reg_in(orig.expr,[args[assigns_to]])
                    if wrote_copy | wrote_orig:
                        return optimised

        return optimised
                            

    def suboptimisation(self):
        """ triggers propagate_from_move() when move instruction found """

        self.logger = logging.getLogger('CopyPropagation')
        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                optimised = self.propagate_from_move(i, ins, optimised)
        return optimised



class DeadCode(BlockOptimiser):
    """ 
    finds and removes instructions that assign a value that is then never used.  
    
    """

    def j_thirty_one_present(self):
        """ 
        (unimplemented) returns true if a j$31 instruction is present in
        block 
        
        """

        for instruction in self.block:

            if not isinstance(instruction,Instr):
                continue
            elif str(instruction.instr) == 'j':
                arg = instruction.args[0]
                if isinstance(arg, str):
                    if arg == '$31':
                        return True
                else:
                    if arg == '$31':
                        return True

        return False
            

    def jal_present(self):
        """ 
        (unimplemented) returns true if a j$31 instruction is present in
        block 
        
        """

        for instruction in self.block:
            if not isinstance(instruction,Instr):
                continue
            elif str(instruction.instr) == 'jal':
                return True
        return False


    def subscan(self, i, ins, opt, cand_reg_index):
        """ 
        searches subsequent instructions, and: stops if candidate register is
        used; or removes the candidate instruction if register is overwritten;
        note: the only instruction object without an args attribute is the nop
        instruction, and such instructions are ignored; note also, certain
        registers not candidates due to being used for function parameters or
        other more permanent values

        """

        optimised = opt

        for i2, ins2 in enumerate(self.peephole[i+1:len(self.peephole)]):

            candidate_reg = ins.args[cand_reg_index]
            ins2_is_instruction = isinstance(ins,Instr)
            args = []

            if not ins2_is_instruction:
                continue

            try:
                for arg in ins2.args:
                    if isinstance(arg,str) | isinstance(arg,int) :
                        args.append(arg)
                    else:
                        args.append(arg.expr)
            except AttributeError:
                continue

            if not self.reg_in(candidate_reg.expr, args):
                continue

            elif str(ins2.instr) in assign_to:
                assigned_to_index = assign_to[str(ins2.instr)]
                pre_args = args[0:assigned_to_index]
                post_args = args[assigned_to_index+1:len(args)]
                if self.reg_in(candidate_reg.expr,pre_args+post_args):
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
        """ 
        triggers subscan() for every peephole instruction in assign_to
        category; aborts if jal or j $31 instruction in block
        
        """
        
        optimised = False
        if (self.j_thirty_one_present()) | (self.jal_present()):
            return optimised
        self.logger = logging.getLogger('DeadCode')
        candidate = None
        for i, ins in enumerate(self.peephole):
            if not isinstance(ins,Instr):
                continue
            elif str(ins.instr) in assign_to:
                cand_reg_index = assign_to[str(ins.instr)]
                optimised = self.subscan(i, ins, optimised, cand_reg_index)
        return optimised



class ConstantFold(BlockOptimiser):
    """ 
    replaces arithmetic instructions with only compile-time constants in
    arguments, with a load immediate instruction to assign the corresponding
    value to the same target register 
    
    """


    def addu(self, i, ins, opt, consts):
        """ 
        carries out constant folding on addu instructions; though not guaranteed
        to replicate unsigned behaviour, this should be ok for our benchmarks;
        note that addu's, as manifest in benchmark suite, seem to incorporate
        addiu functionality since no addiu's are present, and at least one
        instance of a compile-time value was found in the arguments of an addu
        instruction, in the benchmark suite
        
        """    

        optimised = opt

        if ins.instr == 'addu':

            arg1_is_reg = isinstance(ins.args[1],ir.Register)
            arg2_is_reg = isinstance(ins.args[2],ir.Register)
            none_reg = (not arg1_is_reg) & (not arg2_is_reg)
            arg1_known_reg = False
            arg2_known_reg = False

            if arg1_is_reg:
                arg1_known_reg = (self.reg_in(ins.args[1].expr, consts))
            if arg2_is_reg:
                arg2_known_reg = (self.reg_in(ins.args[2].expr, consts))

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
        """ tries to constant-fold if 2+ compile time constants present """

        self.logger = logging.getLogger('ConstantFold')
        optimised = False

        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                consts = self.find_constants(i)
                if len(consts) > 1:
                    optimised = self.addu(i, ins, optimised, consts)
        return optimised
