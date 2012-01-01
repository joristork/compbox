""" 
File:         uic.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam

The "useful instruction categories" module

Description:
    blah

"""


"""
Instructions (keys) that respectively assign to the registers in
args[(values)]

"""
assign_to = {
    'abs.d' :   0   ,
    'abs.s' :   0   , 
    'add'   :   0   ,
    'add.d' :   0   , 
    'addu'  :   0   ,
    'add.s' :   0   ,
    'and'   :   0   ,
    'cvt.d.w':  0   ,
    'cvt.d.s':  0   ,
    'cvt.s.d':  0   ,
    'cvt.s.w':  0   ,
    'cvt'   :   0   ,  
    'c.s'   :   0   ,     
    'c.d'   :   0   , 
    'divu'  :   0   ,
    'sub.u' :   0   ,
    'sub.d' :   0   ,
    'add.d' :   0   ,
    'div.d' :   0   ,
    'div.s' :   0   ,
    'div'   :   0   ,
    'dlw'   :   0   ,
    'lb'    :   0   ,
    'l.s'   :   0   ,
    'l.d'   :   0   ,
    'l.a'   :   0   ,
    'li'    :   0   ,
    'lw'    :   0   ,
    'lbu'   :   0   ,
    'lh'    :   0   ,
    'lhu'   :   0   ,
    'move'  :   0   ,
    'mov.d' :   0   ,
    'mov.s' :   0   ,
    'mult'  :   0   , 
    'mult.s':   0   , 
    'mult.d':   0   , 
    'multu' :   0   , 
    'neg.s' :   0   ,  
    'neg.d' :   0   ,
    'nor'   :   0   ,
    'or'    :   0   ,
    'sra'   :   0   ,
    'sub.s' :   0   ,
    'subu'  :   0   ,
    'sub'   :   0   ,
    'srl'   :   0   ,
    'sll'   :   0   ,
    'sra'   :   0   ,    
    'slt'   :   0   , 
    'sqrt.s':   0   ,  
    'sqrt.d':   0   , 
    'sltu'  :   0   , 
    'xor'   :   0   ,
    'xori'  :   0   
    }


""" 
These instruction types may be subject to substituting copy references with
original references as part of a copy propagation optimisation

"""
copy_prop_targets = [
    'add',      #- integer add 
    'addu',     #- integer add unsigned 
    'add.s',    #- single-precision (SP) add
    'add.d',    #- double-precision (DP) add
    'and',      #- logical AND 
    'beq',   #- branch == 0 
    'bne',   #- branch != 0 
    'blez',  #- branch <= 0 
    'bgtz',  #- branch > 0 
    'bltz',  #- branch < 0 
    'bgez',  #- branch >= 0 
    'bc1f',   #- Branch on floating point compare false.
    'bc1t',   #- Branch on floating point compare true.
    'cvt',       #- int., single, double conversion
    'c.s',      #- SP compare
    'c.d',      #- DP compare
    'dsw',  #- store double word 
    'div',      #- integer divide 
    'divu',     #- integer divide unsigned 
    'dlw',  #- load double word 
    'or',       #- logical OR 
    'nor',      #- logical NOR 
    'srl',      #- shift right logical 
    'sra',      #- shift right arithmetic 
    'slt',      #- set less than 
    'sltu',     #- set less than unsigned 
    'sub.s',    #- SP subtract
    'sub.d',    #- DP subtract
    'div.s',    #- SP divide
    'div.d',    #- DP divide
    'abs.s',    #- SP absolute value
    'abs.d',    #- DP absolute value
    'neg.s',    #- SP negation
    'neg.d',    #- DP negation
    'cvt',      #- int., single, double conversion
    'c.s',      #- SP compare
    'c.d',      #- DP compare
    'jr',    #- jump register 
    'jalr',  #- jump and link register 
    'lb',   #- load byte 
    'lbu',  #- load byte unsigned 
    'lh',   #- load half (short) 
    'lhu',  #- load half (short) unsigned 
    'lw',   #- load word 
    'l.s',  #- load single-precision FP 
    'l.d',  #- load double-precision FP 
    'li'
    'move', # extra
    'mult.s',   #- SP multiply
    'mult.d',   #- DP multiply
    'mult',     #- integer multiply 
    'multu',    #- integer multiply unsigned 
    'nor',  #- logical NOR 
    'or',   #- logical OR 
    'sll',      #- shift left logical 
    'srl',  #- shift right logical 
    'sra',  #- shift right arithmetic 
    'slt',  #- set less than 
    'sltu', #- set less than unsigned 
    'sub',      #- subtract 
    'subu',     #- integer subtract unsigned 
    'sub.s',    #- SP subtract
    'sub.d',    #- DP subtract
    'sqrt.s',   #- SP square root
    'sqrt.d',   #- DP square root
    'sb',   #- store byte 
    'sbu',  #- store byte unsigned 
    'sh',   #- store half (short) 
    'shu',  #- store half (short) unsigned 
    'sw',   #- store word 
    's.s',  #- store single-precision FP 
    's.d',  #- store double-precision FP
    'xor'      #- logical XOR 
    ]


""" 
If copy propagate optimiser encounters one of these instructions during a
scan of instructions below a copy, no instructions beyond that instruction
may be considered safe 

"""
copy_prop_unsafe = [
    'mflo',
    'mtcl',
    'la',
    'mfc1',
    'dmfc1',
    ]
