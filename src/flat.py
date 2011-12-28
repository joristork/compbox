#!/usr/bin/env python

from asmyacc import parser
import sys
from ir import *

#test with: optimize([Instr("BEQ", ["2"]), Label("1"),Label("2"),Instr("j",["3"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Instr("BEQ", ["2"]),Label("3")])

    
def optimize_jump(instruction_list):
    """
    This function scans the instruction list to make improvements by adjusting
    and removing jumps and labels.
    Situations:     Label, Jump
                    Jump, NOT Label
                    label, label
    First we need to scan the list for jump_not_label. After this has
    been done, we can start on label_label and label_jump imporvements.
    """
    instruction_list = remove_comments(instruction_list)
    clean = False
    while(not clean):
        clean = True    
        for i,instruction in enumerate(instruction_list):
            clean = jump_not_label(instruction, i, instruction_list)
            if not clean:
                break
    clean = False
    while(not clean):
        clean = True                
        for i,instruction in enumerate(instruction_list):    
            clean = label_label(instruction, i, instruction_list)
            if not clean:
                break            
            clean = label_jump(instruction, i, instruction_list)
            if not clean:
                break

    return instruction_list


def remove_comments(il):
    new = []
    for ins in il:
        if type(ins) != Comment:
            new.append(ins)
    return new

def jump_not_label(ins, i, il):
    """
    Every instruction that is between a jump and a label will never be
    executed. This function removes all the instructions that never will be
    executed.
    """
    clean = True
    if (type(ins) == Instr and
        ins.instr.lower() == 'j'):
            while (i < len(il) - 1 and
                   type(il[i + 1]) != Label and type(il[i + 1]) != Raw):
                del il[i + 1]
                if clean:
                    clean = False
    return clean

def label_label(label, i , il):
    """
    This function searches for labels, and removes all labels that come
    directly after it. The instructions that point to one of the removed
    labels are adjusted so that they point to the first label, that isn't
    removed.
    """
    clean = True
    if (type(label) == Label):
        while (i < len(il) - 1 and
                type(il[i + 1]) == Label):
            replace_label(label.expr, il[i + 1].expr, il)
            del il[i + 1]
            clean = False
    return clean

def label_jump(ins, i, il):
    """
    If a jump comes directly after a label, the label as well as the jump are
    unneccesery. All instructions point to the label are adjusted to point to
    the label the jump was pointing at. 
    """
    clean = True
    if i < len(il) - 1:
        next_i = il[i + 1]
        if (type(ins) == Label and
            type(il[i + 1]) == Instr and
            il[i + 1].instr.lower() == 'j'):
                replace_label(il[i + 1].args[0], ins.expr, il)
                del il[i:i + 2]
                clean = False
    return clean
    

def replace_label(new_label, old_label, il):
    """
    This helper function adjusts all instructions that point to the old_label
    so that they point to the new label.

    IMPORTANT: Make sure new_label and old_label are strings. For instructions
    the correct string is Instr.args[i] for some i and for Labels the correct
    string is Label.expr .
    """
    for ins in il:
        if (type(ins) == Instr):
            while (old_label in ins.args):
                ins.args[ins.args.index(old_label)] = new_label

def optimize_brench(instruction_list):
    instruction_list = brench_jump(instruction_list)
    instruction_list = useless_brench(instruction_list)
    return instruction_list
   
def useless_brench(il):
    """
    If a jump or brench points to a label that comes directly after it, it can be
    removed.
    """
    clean = False
    while(not clean):
        clean = True    
        for i,ins in enumerate(il):
            if type(ins) == Instr and i < len(il) - 1 and \
               type(il[i + 1]) == Label and \
               ins.instr.lower() in control_instructions:
                if ins.jump_dest() == il[i + 1].expr:
                    del il[i]
                    clean = False
                    break
                
    return il
    
    
def brench_jump(il):
    """
    This function removes a jump when we find a brench - jump - label
    combination where the brench points to the label. We can optimize this
    by negating the brench, making it point to the jump adres and removing the
    label.
    """
    negation = {'beq':'bne','bne':'beq','blez':'bgtz','bgtz':
        'blez','bltz':'bgez','bgez':'bltz','bc1t':'bc1f','bc1f':'bc1t'}
    clean = False
    while(not clean):
        clean = True  
        for i,ins in enumerate(il):
            if type(ins) == Instr and ins.instr.lower() in negation \
               and i + 2 < len(il) - 1 and type(il[i+1]) == Instr \
               and type(il[i+2]) == Label and \
               ins.jump_dest() == il[i+2].expr:
                il[i].instr = negation[il[i].instr]
                il[i].args[-1] = il[i+1].jump_dest()
                del il[i+1]
                clean = False
                break
            
            
    return il
                
    
def optimize(instruction_list):
    """
    This functions calls a number of flat optimalization routines and
    returns the improved list.
    """
    
    instruction_list = optimize_jump(instruction_list)
    instruction_list = optimize_brench(instruction_list)
    return instruction_list
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        raise_on_error = True
        instruction_list = []
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           instruction_list.append(parser.parse(line))

        instruction_list = optimize(instruction_list)
        for ins in instruction_list:
            if type(ins) == Label:
                print ins
            elif type(ins) != Comment:
                print "\t" + str(ins)
