""" 
File:         optimise.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam


Description:
    This file contains two optimalisations that can be done on a graph:
        - remove not used (removes all blocks that can't be reached)
        - flatten (merges blocks so that there are less jumps)

"""

import cfg
from ir import *


def optimise(graph):
    """
    Runs various optimisation schemes on the cfg
    """
    graph = remove_notused(graph)
    graph = flatten(graph)
    return graph

def remove_notused(graph):
    """
    All blocks that have no incoming edges are removed.
    Ofcourse the starting block is ignored, as well as
    the block that only contains a raw .end instruction.
    """
    for (i, block) in enumerate(graph.blocks):
        if i != 0 and len(graph.get_in_edges(block)) == 0:
            for instr in block.instructions:
                if type(instr) == Instr:
                    block.instructions.remove(instr)
            if len(block.instructions) == 0:
                graph.remove_block(block)
            
                
    return graph

def flatten(graph):
    """
    If a block has only one incoming edge and the block on the other side of the edge
    has only one outgoing edge, the blocks can be joined into one.

    After this, jump optimalisation is needed.
    """
    clean = False
    while(not clean):
        clean = True
        length = len(graph.blocks)
        for i in xrange(length - 1):
            
            te = graph.get_in_edges(graph.blocks[i + 1])
            
            if len(te) == 1:
                et = graph.get_out_edges(te[0][0])
                if len(et) == 1:
                    een = graph.get_block(te[0][0])
                    twee = graph.blocks[i + 1]
                    td = graph.get_out_edges(twee)

                    een.instructions = een.instructions + twee.instructions
                    for (fr, to) in td:
                        graph.edges.append((een.name, to))

                    graph.remove_block(twee.name)
                    clean = False
                    break

    return graph


def main():
    c = cfg.main()
    c.cfg_to_diagram("cfg_org.png")
    c = optimise(c)
    c.cfg_to_diagram("cfg_new.png")
    return c
if __name__ == '__main__':
    main()
    pass
