# Test of parsing en code generation correct is.

import unittest
import sys
sys.path.append("../") 

import optimise


class TestNoOpt(unittest.TestCase):

    def test_no_opt_bench(self):
        path = 'nullsource/'
        for sourcefilename in ('slalom.s.opt', 'acron.s.opt', 'clinpack.s.opt',
                'pi.s.opt', 'whet.s.opt', 'dhrystone.s.opt'):
            sourcefile = open(path + sourcefilename)
            source = sourcefile.readlines()
            sourcefile.close()

            opt = optimise.Optimiser(source, 0, True)

            opt.optimise()

            self.assertEqual(source, opt.result())

if __name__ == '__main__':
    unittest.main()
