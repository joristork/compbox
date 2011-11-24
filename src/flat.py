#!/usr/bin/env python

import asmyacc
import sys
from ir import *

def optimize_jump(instruction_list):
    """
        Situations:     Label, Jump
                        Jump, NOT Label
                        label, label
    """
    for i,instruction in enumerate(instruction_list):        
            jump_not_label(instruction, i, instruction_list)
    for i,instruction in enumerate(instruction_list):
            label_jump(instruction, i, instruction_list)
            
            
    return instruction_list

def label_jump(instruction, i, instruction_list):
    if i < len(instruction_list) - 1:
        next_i = instruction_list[i + 1]
        if (type(instruction) == Label and
            type(next_i) == Instr and
            next_i.instr == 'j'):
                replace_label(next_i.args[0], instruction.expr, instruction_list)
                instruction_list.remove(instruction)
                instruction_list.remove(next_i)    
                    
def jump_not_label(ins, i, il):
    if (i < len(il) - 1 and
        type(ins) == Instr and
        ins.instr == 'j'):
            while (type(il[i + 1]) != Label):
                il.remove(il[i + 1])

def replace_label(new_label, old_label, il):
    for instruction in il:
        if (type(instruction) == Instr and old_label in instruction.args):
            instruction.args.insert(instruction.args.index(old_label), new_label)
            instruction.args.remove(old_label)
    

    
def optimize_flat(instruction_list):
    instruction_list = optimize_jump(instruction_list)
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        raise_on_error = True
        instruction_list = []
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           instruction_list.append(asmyacc.parser.parse(line))   
        optimize_flat(instruction_list)
