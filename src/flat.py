#!/usr/bin/env python

from asmyacc import parser
import sys
from ir import *

#test with: optimize_jump([Instr("BEQ", ["2"]), Label("1"),Label("2"),Instr("j",["3"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Label("3")])

def optimize_jump(instruction_list):
    """
        Situations:     Label, Jump
                        Jump, NOT Label
                        label, label
    """
    for i,instruction in enumerate(instruction_list):        
            jump_not_label(instruction, i, instruction_list)
    for i,instruction in enumerate(instruction_list):        
            label_label(instruction, i, instruction_list)
            label_jump(instruction, i, instruction_list)

    return instruction_list

def jump_not_label(ins, i, il):
    """
    Every instruction that is between a jump and a label will never be
    executed. This function removes all the instructions that never will be
    executed.
    """
    if (type(ins) == Instr and
        ins.instr == 'j'):
            while (i < len(il) - 1 and
                   type(il[i + 1]) != Label):
                del il[i + 1]

def label_label(ins, i , il):
    """
    This function searches for labels, and removes all labels that come
    directly after it. The instructions that point to one of the removed
    labels are adjusted so that they point to the first label, that isn't
    removed.
    """
    if (type(ins) == Label):
        while (i < len(il) - 1 and
                type(il[i + 1]) == Label):
            
            replace_label(ins, il[i + 1], il)
            del il[i + 1]

def label_jump(ins, i, il):
    """
    If a jump comes directly after a label, the label as well as the jump are
    unneccesery. All instructions point to the label are adjusted to point to
    the label the jump was pointing at. 
    """
    if i < len(il) - 1:
        next_i = il[i + 1]
        if (type(ins) == Label and
            type(il[i + 1]) == Instr and
            il[i + 1].instr == 'j'):
                replace_label(il[i + 1].args[0], ins.expr, il)
                del il[i:i + 2]    

def replace_label(new_label, old_label, il):
    """
    This helper function
    """

    
    for ins in il:
        if (type(ins) == Instr):
            while (str(old_label).strip() in str(ins.args).strip()):
                ins.args[ins.args.index(str(old_label))] = str(new_label)











    
def optimize_flat(instruction_list):
    instruction_list = optimize_jump(instruction_list)
    return instruction_list
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        raise_on_error = True
        instruction_list = []
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           instruction_list.append(asmyacc.parser.parse(line))   
        optimize_flat(instruction_list)
