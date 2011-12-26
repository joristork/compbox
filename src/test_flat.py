#!/usr/bin/env python
import unittest
import flat
from ir import *


class TestFlatOptimizer(unittest.TestCase):
    insls = []
    def setUp(self):
        self.insls = [[Instr("BEQ", ["2"]), 
        Label("1"),
        Label("2"),
        Instr("j",["3"]),
        Instr("BEQ", ["2"]),
        Instr("BEQ", ["2"]),
        Instr("BEQ", ["2"]),
        Instr("BEQ", ["2"]),
        Instr("BEQ", ["2"]),
        Label("3")]]
        
    def test_optimize_jump(self):
        results = []
        for insl in self.insls:
            results.append(flat.optimize_jump(insl))
         
        exps = ["[<Instr 'BEQ' ['3']>, <Label '3'>]"]
        self.assertTrue(len(exps)==len(results))
        for res,exp in zip(results, exps):
            self.assertEqual(str(res), exp)
        
        
    

if __name__ == '__main__':
    unittest.main()
