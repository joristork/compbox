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
    list_length = len(instruction_list)
    for i,instruction in enumerate(instruction_list):
        if i < list_length - 1:
            next_i = instruction_list[i + 1]
            if (type(instruction) == Label and
                type(next_i) == Instr and
                next_i.instr == 'j'):
                    replace_label(next_i.args[0], instruction.expr, instruction_list)
                    instruction_list.remove(instruction)
                    instruction_list.remove(next_i)
            #if (type(instruction) == Instr and
            #    instruction.instr == 'j' and
            #    type(next_i) != Label):
            #    while (type(rm_i) != Label):
    return instruction_list       
                

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
