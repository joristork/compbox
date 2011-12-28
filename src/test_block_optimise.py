#! /usr/bin/env python
import unittest
import block_optimise
import ir
import cfg


class TestBlockOptimisers(unittest.TestCase):
    """ unittests for the block_optimise module  """


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_algebra(self):
        i0 = ir.Instr('div.d', ['dest',1634563464,64])
        block = cfg.BasicBlock([i0])
        bop = block_optimise.AlgebraicTransformations(block = block)
        bop.optimise()
        expected = str(ir.Instr('sra', ['dest', 1634563464, 6.0]))
        result = str(block[0])
        #TODO: map assertion to list of (expected,result)
        self.assertTrue(result == expected)


    def test_const_fold_addu(self):
        instrs = [ir.Instr('filler', ['dest',1634563464,64])]
        instrs.append(ir.Instr('li', ['dest1', 0x0001]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('li', ['dest2', 0x0002]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['adest1','dest1','dest2']))
        instrs.append(ir.Instr('li', ['dest3', 0x0003]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['adest2','adest1','dest3']))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        block = cfg.BasicBlock(instrs)
        bop = block_optimise.ConstantFold(block = block)
        bop.optimise()
        expected = str(ir.Instr('li', ['adest2', 0x6]))
        result = str(block[8])
        #print 'result[8]: ',result
        self.assertTrue(result == expected)


if __name__ == '__main__':
    unittest.main()
