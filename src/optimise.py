#!/usr/bin/env python

#
# optimise.py
#

import sys

# Option parsing module:
# from optparse import OptionParser

# Our own Optimiser modules:
# import modules


class Optimiser(object):
    """
    Main Optimiser.

    Tasks
     - convert source to IR;
     - let Optimiser modules optimise the IR;
     - convert IR back to source.
    """
    
    def __init__(self, lines):
        print 'Optimiser\nsource: %s' % lines


def main():
    """ Parse command line args, init. optimiser and run optimisations. """

    # Use plain sys.argv[1] for now. optparse is for later.
    if len(sys.argv) != 2:
        print "argument expected"
        return
    sourcefile = open(sys.argv[1], 'r')
    opt = Optimiser(sourcefile.readlines())
    sourcefile.close()


if __name__ == '__main__':
    main()

    
    
    
