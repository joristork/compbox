from cfg import CFG, BasicBlock
from ir import *


class Liveness(object):
    def __init__(self, graph):
        self.graph = graph

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/pi.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
    c = CFG(flat)
    for inst in flat:
        if type(inst)==Register:
            print inst

    
    return c
if __name__ == '__main__':
    main()
    pass
