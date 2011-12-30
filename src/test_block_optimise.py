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
        instrs = [ir.Instr('li', ['dest1', 1634563464])]
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('li', ['dest2', 64]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('div.d', ['divdest1','dest1','dest2']))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        block = cfg.BasicBlock(instrs)
        bop = block_optimise.AlgebraicTransformations(block = block)
        bop.optimise()
        expected = str(ir.Instr('sra', ['divdest1', 1634563464, 6.0]))
        result = str(block[4])
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
        #print 'result: ',result
        self.assertTrue(result == expected)


    def test_copyprop_move(self):
        instrs = [ir.Instr('filler', ['dest',1634563464,64])]
        instrs.append(ir.Instr('move', ['copy1', 'orig1']))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['adest1','copy1','somereg']))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['copy1','somereg','copy1']))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['adest2','copy1','somereg']))
        block = cfg.BasicBlock(instrs)
        bop = block_optimise.CopyPropagation(block = block)
        bop.optimise()
        expected1 = str(ir.Instr('addu', ['adest1', 'orig1', 'somereg']))
        result1 = str(block[3])
        expected2 = str(ir.Instr('addu', ['copy1', 'somereg', 'orig1']))
        result2 = str(block[5])
        expected3 = str(ir.Instr('addu', ['adest2', 'copy1', 'somereg']))
        result3 = str(block[7])
        self.assertTrue(result1 == expected1)
        self.assertTrue(result2 == expected2)
        self.assertTrue(result3 == expected3)



if __name__ == '__main__':
    unittest.main()
