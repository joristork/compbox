import unittest

class TestBlockOptimisers(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testAlgebra
        i0 = Instr('div', ['dest',1634563464,64])
        block = BasicBlock([i0])
        print 'input', block.get_instructions(0,len(block)), '\n'
        bop = AlgebraicTransformations(block = block)
        bop.optimise()
        print 'output', block.get_instructions(0,len(block)), '\n'
