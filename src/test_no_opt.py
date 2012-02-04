# Test of parsing en code generation correct is.

import unittest

import optimise


class TestNoOpt(unittest.TestCase):

    def test_no_opt_bench(self):
        path = '../benchmarks/'
        for sourcefilename in ('slalom.s.null', 'acron.s.null', 'clinpack.s.null',
                'pi.s.null', 'whet.s.null', 'dhrystone.s.null'):
            sourcefile = open(path + sourcefilename)
            source = sourcefile.readlines()
            sourcefile.close()

            opt = optimise.Optimiser(source, 0, '' )

            opt.optimise()

            self.assertEqual(source, opt.result())

if __name__ == '__main__':
    unittest.main()
