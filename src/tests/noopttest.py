# Test of parsing en code generation correct is.

import sys
sys.path.append("../") 

import optimise

for sourcefilename in ('slalom.s.opt', 'acron.s.opt', 'clinpack.s.opt', 'pi.s.opt', 'whet.s.opt', 'dhrystone.s.opt'):
    sourcefile = open(sourcefilename)
    source = sourcefile.readlines()
    sourcefile.close()

    opt = optimise.Optimiser(source, 0, True)

    opt.optimise()

    print source == opt.result()
