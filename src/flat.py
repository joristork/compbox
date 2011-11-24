#!/usr/bin/env python

import amsyacc

def optimize_jump(instruction_list):
    for i,instruction in enumerate(instruction_list):
        
    
def optimize_flat(instruction_list):
    instruction_list = optimize_jump(instruction_list)
    
if __main__ == '__main__':
    if len(sys.argv) > 1:
        raise_on_error = True
        instruction_list = []
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           istruction_list.append(amsyacc.parser.parse(line))
        print 'errors: %d\n' % error_count    
        optimize_flat(instruction_list)
