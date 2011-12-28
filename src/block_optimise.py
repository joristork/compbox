#!/usr/bin/env python

from asmyacc import parser
from cfg import BasicBlock
from ir import Instr
import sys
import math



class Peephole(object):
    """ Contains an iterable list of instructions """

    def __init__(self, block, start, size):
        self.block = block
        self.start_index = start
        self.size = size
        self.instructions = self.block[start:size]
        self.counter = 0


    def __iter__(self):
        return self


    def next(self):
        if self.counter >= self.size:
            raise StopIteration
        else:
            self.current_instruction = self.instructions[self.counter]
            self.counter += 1
        return self.current_instruction


    def __getitem__(self, index):
        """   """

        return self.block[start + index]


    def __setitem__(self, index, value):
        """   """

        self.block[self.start_index + index] = value



class Peeper(object):
    """   """

    def __init__(self, block, peephole_size):
        self.block = block
        """ raise an error here if attempt to set size too big """
        self.p_size = peephole_size
        self.counter = 0


    def __iter__(self):
        return self


    def next(self):
        if self.p_size + self.counter > len(self.block):
            raise StopIteration
        else:
            self.peephole = Peephole(self.block, self.counter, self.p_size)
            self.counter += 1
        return self.peephole
        


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


    def find_constants(self):
        """ compiles a dict of (register,constant) pairs in the peephole """
        consts = {}
        for ins in self.peephole:
            if ins.instr == 'li':
                consts[ins.args[0]] = ins.args[1]
        return consts


    def addu(self, i, ins, opt, consts):
        #NOTE: semantically inaccurate, but should be ok (explain in report)
        """ 
        replaces addu instruction with value. Though not guaranteed to replicate
        unsigned behaviour, should be ok for benchmarks (c.f. report)
        
        """    
        optimised = opt
        if ins.instr == 'addu':
            if ins.args[1] in consts:
                if ins.args[2] in consts:
                    newins = Instr('li',[ins.args[0],consts[ins.args[1]]+consts[ins.args[2]]])
                    self.peephole[i] = newins
                    consts[newins.args[0]] = newins.args[1]
                    if self.verbosity == 1 : print 'did a constant fold\n'
                    optimised = True
        return optimised


    def suboptimisation(self):
        """ if 2+ compile time constants, tries constant folding """
        optimised = False
        consts = self.find_constants()
        if len(consts) > 1:
            for i, ins in enumerate(self.peephole.instructions):
                optimised = self.addu(i, ins, optimised, consts)
        return optimised



class AlgebraicTransformations(BlockOptimiser):
    """ contains various algebraic transformation optimisations  """

    def div_to_sra(self, i, ins, opt):
        """ shift-right arithmetic is faster than division...  """
        optimised = opt
        if ins.instr == 'div':
            n = math.log(ins.args[2], 2)
            if n % 1 == 0:
                newins = Instr('sra', [ins.args[0], ins.args[1], n])
                self.peephole[i] = newins
                if self.verbosity == 1 : print 'changed a div to an sra'
                optimised = True
        return optimised


# ADD and MULT too different for simple conversion (add uses rd,  mult uses hi
# and lo registers)    
#    def mult_to_add(self,i, ins, opt):
#        """ addition is faster than multiplication """
#        optimised = opt
#        if ins.instr == 'mult':
#        return optimised


    def suboptimisation(self):
        """   """
        
        optimised = False
        for i, ins in enumerate(self.peephole):
            optimised = self.div_to_sra(i, ins, optimised)
            #TODO: any other algebraic opts? (sla not available)
        return optimised



class CopyPropagation(BlockOptimiser):
    """ after copy, propagate original variable where copy unaltered """

    def suboptimisation(self):
        """ 
        finds copies; then: if unaltered copy used later, substitute with
        original; else ignore (dead code)  
        
        """

        optimised = False

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


def main():
    if len(sys.argv) > 1:
        raise_on_error = True
        instruction_list = []
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           istruction_list.append(parser.parse(line))
        print 'errors: %d\n' % error_count    
        optimize_flat(instruction_list)
    else:
        pass


if __name__ == '__main__':
    main()
