""" 
File:         block_opt_lab.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam


Description:
    Block optimisers not ready for prime-time.

"""

from cfg import BasicBlock
import ir
from ir import Instr
import math
from peephole import Peephole, Peeper
from uic import copy_prop_targets, copy_prop_unsafe, assign_to
import logging


class AlgebraicTransformations(BlockOptimiser):
    """ contains various algebraic transformation optimisations  """


    def divd_to_sra(self, i, ins, opt, consts):
        """ 
        shift-right arithmetic is faster than division... 
        Needs fixing: div.d only ever uses $fn (floating point) registers. li
        instructions (used to find constants) only use $n registers. Note that
        manual states that div instructions write to hi and lo registers,
        whereas benchmark code makes use of an fd register.
       
       """
        optimised = opt
        if ins.instr == 'div.d':
            if (ins.args[1].expr in consts) & (ins.args[2].expr in consts):
                n = math.log(consts[ins.args[2].expr], 2)
                if n % 1 == 0:
                    newins = Instr('sra', [ins.args[0], consts[ins.args[1].expr], n])
                    self.peephole[i] = newins
                    self.logger.info('algebraic transformed (div->sra)')
                    optimised = True
        return optimised


    def suboptimisation(self):
        """   """
        
        self.logger = logging.getLogger('AlgebraicTransformations')
        optimised = False
        for i, ins in enumerate(self.peephole):
            if isinstance(ins,Instr):
                consts = self.find_constants(i)
                #optimised=self.divd_to_sra(i, ins, optimised, consts)#cf shelf 
                #TODO: any other algebraic opts? (sla not available)
        return optimised



class CommonSubexpressions(BlockOptimiser):
    """ Block optimisation: duplicate subexpressions -> variables"""

    def suboptimisation(self):
        """ If duplicate subexpression found within peephole,  """

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
