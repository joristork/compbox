#!/usr/bin/env python

from asmyacc import parser
import cfg



class Peephole(object):
    """ Contains an iterable list of instructions """

    def __init__(self, start, size):
        self.start_index = start_index
        self.size = size
        self.instructions = self.block.get_instructions(start, size))
        self.counter = 0


    def __iter__(self):
        return self


    def next(self):
        if self.counter >= self.size:
            raise StopIteration
        else:
            self.current_instruction = self.instructions[counter]
            self.counter += 1
        return self.current_instruction


    def __getitem__(self, index):
        """   """
        return self.instructions[index]


    def __setitem__(self, index, value):
        """   """
        self.block.set_intruction(self.start_index + index, value)



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
        if self.p_size + self.counter > self.block.length():
            raise StopIteration
        else:
            self.current_peephole = Peephole(self.counter, self.p_size)
            self.counter += 1
        return self.current_peephole
        


class BlockOptimiser(object):
    """ Parent class for the various block optimisations.  """

    def __init__(self, block = None, peephole_size = 3):
        self.block = block
        self.p_size = peephole_size


    def set_block(self, block):
        """ Optimiser can be re-assigned to a new block  """
        self.block = block


    def set_peephole_size(self, size):
        """ Optimiser can be tweaked with a new peephole size. """
        self.p_size = size


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
            while suboptimisation(peephole):
                pass



class CommonSubexpressions(BlockOptimiser):
    """ Block optimisation: duplicate subexpressions -> variables"""

    def suboptimisation(self, peephole):
        """   """
        return False



class ConstantFold(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



class CopyPropagation(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



class DeadCode(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



class TempVarRename(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



class ExchangeIndependentStatements(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



class AlgebraicTransformations(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



class MachineDependentTransformations(BlockOptimiser):
    """   """

    def suboptimisation(self, peephole):
        """   """
        return False



if __main__ == '__main__':
    if len(sys.argv) > 1:
        raise_on_error = True
        instruction_list = []
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           istruction_list.append(parser.parse(line))
        print 'errors: %d\n' % error_count    
        optimize_flat(instruction_list)
