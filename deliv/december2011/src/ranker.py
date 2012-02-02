#!/usr/bin/env python
""" 
File:         ranker.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam

The peephole module

Description:
    A little utility to compile a dict that ranks the instructions in the
    benchmark suite by incidence. Opcodes are keys, with the numbers of
    occurrences of the instruction in the benchmark suite stored in the
    corresponding dict value. 

"""

from optparse import OptionParser
from asmyacc import parser
import ir
from operator import itemgetter


class Ranker(object):
    
    def __init__(self):
        self.flat = []
        self.rankingdict = {}
        self.ranking = None

    def addlines(self, lines):
        for line in lines:
            if not line.strip():
                continue
            self.flat.append(parser.parse(line))


    def rank(self):
        for line in self.flat:
            if isinstance(line, ir.Instr):
                if line.instr in self.rankingdict:
                    self.rankingdict[line.instr] = self.rankingdict[line.instr] + 1
                else:
                    self.rankingdict[line.instr] = 1
        self.ranking = sorted(self.rankingdict.iteritems(), key=itemgetter(1), reverse=True)
        print self.ranking

    
    def result(self):
        return [str(instr)+'\n' for instr in self.ranking]


def main():
    sourcefiles = []
    ranker = Ranker()
    filelist = ['acron.s', 'clinpack.s', 'dhrystone.s', 'pi.s', 'slalom.s', 'whet.s']
    for filename in filelist:
        sourcefile = open(('../benchmarks/'+filename), 'r')
        ranker.addlines(sourcefile.readlines())
        sourcefile.close()
    ranker.rank()
    targetfile = open('irank', 'w')
    targetfile.writelines(ranker.result())
    targetfile.close()

if __name__ == '__main__':
    main()

    
    
    
