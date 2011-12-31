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


#    def test_algebra(self):
#        dest1 = ir.Register('$dest1')
#        dest2 = ir.Register('$dest2')
#        divdest1 = ir.Register('divdest1')
#        instrs = [ir.Instr('li', [dest1, 1634563464])]
#        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
#        instrs.append(ir.Instr('li', [dest2, 64]))
#        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
#        instrs.append(ir.Instr('div.d', [divdest1,dest1,dest2]))
#        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
#        block = cfg.BasicBlock(instrs)
#        bop = block_optimise.AlgebraicTransformations(block = block)
#        bop.optimise()
#        expected = str(ir.Instr('sra', [divdest1, 1634563464, 6.0]))
#        result = str(block[4])
#        #TODO: map assertion to list of (expected,result)
#        self.assertTrue(result == expected)


    def test_const_fold_addu(self):
        dest1 = ir.Register('$dest1')
        dest2 = ir.Register('$dest2')
        dest3 = ir.Register('$dest3')
        adest1 = ir.Register('$adest1')
        adest2 = ir.Register('$adest2')
        instrs = [ir.Instr('filler', ['dest',1634563464,64])]
        instrs.append(ir.Instr('li', [dest1, 0x0001]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('li', [dest2, 0x0002]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', [adest1,dest1,dest2]))
        instrs.append(ir.Instr('li', [dest3, 0x0003]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', [adest2,adest1,dest3]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        block = cfg.BasicBlock(instrs)
        bop = block_optimise.ConstantFold(block = block)
        bop.optimise()
        expected = str(ir.Instr('li', [adest2, '0x6']))
        result = str(block[8])
        self.assertTrue(result == expected)


    def test_copyprop_move(self):
        copy1 = ir.Register('$copy1')
        orig1 = ir.Register('$orig11')
        instrs = [ir.Instr('filler', ['dest',1634563464,64])]
        instrs.append(ir.Instr('move', [copy1, orig1]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['$adest1',copy1,'somereg']))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', [copy1,'somereg',copy1]))
        instrs.append(ir.Instr('filler', ['dest',1634563464,64]))
        instrs.append(ir.Instr('addu', ['$adest2',copy1,'somereg']))
        block = cfg.BasicBlock(instrs)
        bop = block_optimise.CopyPropagation(block = block)
        bop.optimise()
        expected1 = str(ir.Instr('addu', ['$adest1', orig1, 'somereg']))
        result1 = str(block[3])
        expected2 = str(ir.Instr('addu', [copy1, 'somereg', orig1]))
        result2 = str(block[5])
        expected3 = str(ir.Instr('addu', ['$adest2', copy1, 'somereg']))
        result3 = str(block[7])
        self.assertTrue(result1 == expected1)
        self.assertTrue(result2 == expected2)
        self.assertTrue(result3 == expected3)


    def test_dead_code(self):
        reg1 = ir.Register('$1')
        reg2 = ir.Register('$2')
        reg3 = ir.Register('$3')
        reg4 = ir.Register('$4')
        reg5 = ir.Register('$5')
        sp = ir.Register('$sp')
        dp = ir.Register('$dp')
        r31 = ir.Register('$31')
        offsetadd1 = ir.Register('20($sp)')
        offsetadd2 = ir.Register('16($sp)')
        instrs = [ir.Instr('filler', ['$filler',1634563464,64])]
        instrs.append(ir.Instr('addu', [reg1,reg2,reg3]))
        instrs.append(ir.Instr('filler2', ['dest',9999,64]))
        instrs.append(ir.Instr('sll', [reg3, reg4, 10]))
        instrs.append(ir.Instr('filler3', ['dest',9999,64]))
        instrs.append(ir.Instr('lw', [reg3, '0(dp)']))
        instrs.append(ir.Instr('filler4', ['dest',9999,64]))
        instrs.append(ir.Instr('addu', [reg1,reg2,reg4]))
        instrs.append(ir.Instr('filler5', ['dest',9999,64]))
        instrs.append(ir.Instr('addu', [reg3,reg1,reg2]))
        instrs.append(ir.Instr('filler6', ['dest',9999,64]))
        instrs.append(ir.Instr('div', [reg1,reg2,reg4]))
        instrs.append(ir.Instr('move', [sp,dp]))
        instrs.append(ir.Instr('lw', [r31, offsetadd1]))
        instrs.append(ir.Instr('lw', [dp, offsetadd2]))
        instrs.append(ir.Instr('addu', [sp,dp,24]))
        block = cfg.BasicBlock(instrs)
        bop = block_optimise.DeadCode(block = block)
        bop.optimise()
        exp_instrs = [ir.Instr('filler', ['$filler',1634563464,64])]
        exp_instrs.append(ir.Instr('filler2', ['dest',9999,64]))
        exp_instrs.append(ir.Instr('filler3', ['dest',9999,64]))
        exp_instrs.append(ir.Instr('filler4', ['dest',9999,64]))
        exp_instrs.append(ir.Instr('addu', [reg1,reg2,reg4]))
        exp_instrs.append(ir.Instr('filler5', ['dest',9999,64]))
        exp_instrs.append(ir.Instr('addu', [reg3,reg1,reg2]))
        exp_instrs.append(ir.Instr('filler6', ['dest',9999,64]))
        exp_instrs.append(ir.Instr('div', [reg1,reg2,reg4]))
        exp_instrs.append(ir.Instr('move', [sp,dp]))
        exp_instrs.append(ir.Instr('lw', [r31, offsetadd1]))
        exp_instrs.append(ir.Instr('lw', [dp, offsetadd2]))
        exp_instrs.append(ir.Instr('addu', [sp,dp,24]))
        for i in xrange(len(block)):
            self.assertTrue(str(block[i]) == str(exp_instrs[i]))



if __name__ == '__main__':
    unittest.main()
