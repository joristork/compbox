#! /usr/bin/env python
"""
unittest_graph.py

A set of unit tests for graph.py

"""

import unittest

from optimise import Graph

class OpTest(object):
    """
    Op for testing

    The syntax of the language that this Op simulates is:

    normal operation:
        <string> <argument>+

    branch:
        control <line nr>

    All branches are conditional.
    """
    
    def __init__(self, expr):
        self.expr = expr
        expr_split = expr.split(' ')
        self.type = expr_split[0]

        self.arguments = expr_split[1]
        if type(self.arguments) == str:
            self.arguments = [self.arguments]

    def get_jump_target_index(self, index):
        return int(self.arguments[0])

    def __repr__(self):
        return 'Op(%s)' % str(self.expr)


def op_iter(blocks):
    for block in blocks:
        for op in block.ops:
            yield op

class GraphTest(unittest.TestCase):



    def test_class(self):
        Graph
        g = Graph
        str(g)
        repr(g)
        g.exit_block
        g.entry_block

    def test_empty_instance(self):
        # empty list
        g = Graph([], OpTest)
        self.assertEqual(len(g.blocks), 0)
        str(g)
        repr(g)
        
    def test_input_one_op(self):
        lines = [
            "op0 x",        #0
            ]
        g = Graph(lines, OpTest)
        str(g)
        repr(g)
        # one block
        self.assertEqual(len(g.blocks), 1)
        # one op in this block
        self.assertEqual(len(g.blocks[0].ops), 1)
        # next is exit, jump is None
        self.assertEqual(g.blocks[0].jump, None)
        self.assertEqual(g.blocks[0].next, Graph.exit_block)

    def test_input_simple_loop(self):
        lines = [
            "op0 x",        #0
            "op1 y",        #1
            "control 0"     #2
            ]
        g = Graph(lines, OpTest)
        # 3 ops
        self.assertEqual(len(list(op_iter(g.blocks))), 3)
        # one block
        self.assertEqual(len(g.blocks), 1)
        # which jumps to itself
        self.assertEqual(g.blocks[0].jump, g.blocks[0])

    def test_input_invalid_jump(self):
        lines = [
            "op0 x",        #0
            "op1 y",        #1
            "control 3"     #2
            ]
        g = Graph(lines, OpTest)
        # 3 ops
        self.assertEqual(len(list(op_iter(g.blocks))), 3)
        # one block
        self.assertEqual(len(g.blocks), 1)
        # which jumps to exit
        self.assertEqual(g.blocks[0].jump, Graph.exit_block)

        # again, slightly different
        lines = [
            "op0 x",        #0
            "op1 y",        #1
            "control 10",   #2
            "op2 z",        #3
            ]
        g = Graph(lines, OpTest)
        # 3 ops
        self.assertEqual(len(list(op_iter(g.blocks))), 4)
        # 2 blocks
        self.assertEqual(len(g.blocks), 2)
        # which jumps to exit
        self.assertEqual(g.blocks[0].jump, Graph.exit_block)
        self.assertEqual(g.blocks[0].next, g.blocks[1])       

    def test_input_mutiple_blocks(self):
        lines = [
            "op0 x",        #0
            "op1 y",        #1
            "control 0",    #2
            "op3 z",        #3
            "op4 x",        #4
            "control 0",    #5
            "op 6 y",       #6
            "op 7 z"        #7
            ]
        g = Graph(lines, OpTest)
        # 8 ops
        self.assertEqual(len(list(op_iter(g.blocks))), 8)
        # 3 blocks
        self.assertEqual(len(g.blocks), 3)
        
        self.assertEqual(g.blocks[0].jump, g.blocks[0])
        self.assertEqual(g.blocks[0].next, g.blocks[1])
        self.assertEqual(g.blocks[1].jump, g.blocks[0])
        self.assertEqual(g.blocks[1].next, g.blocks[2])
        self.assertEqual(g.blocks[2].jump, None)
        self.assertEqual(g.blocks[2].next, Graph.exit_block)

    def test_input_mutiple_blocks_2(self):
        lines = [
            "op0 x",        #0
            "op1 y",        #1
            "control 1",    #2
            "control 2",    #3
            ]
        g = Graph(lines, OpTest)
        # 4 ops
        self.assertEqual(len(list(op_iter(g.blocks))), 4)
        # 4 blocks
        self.assertEqual(len(g.blocks), 4)

        self.assertEqual(g.blocks[0].block_id, 0)
        self.assertEqual(g.blocks[1].block_id, 1)
        self.assertEqual(g.blocks[2].block_id, 2)
        self.assertEqual(g.blocks[3].block_id, 3)

        self.assertEqual(g.blocks[0].jump, None)
        self.assertEqual(g.blocks[1].jump, None)
        self.assertEqual(g.blocks[2].jump, g.blocks[1])
        self.assertEqual(g.blocks[3].jump, g.blocks[2])


if __name__ == '__main__':
    unittest.main()

