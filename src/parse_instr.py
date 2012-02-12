""" 
File:         optimise.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam


Description:
    This file contains all information about the different assembly 
    instructions. When it is used to parse a flat list, all instruction objects
    get a list that contains the register that are needed and another list with
    the registers that are generated.


"""

from ir import *
import re
numreg = re.compile("^(\$[a-z]?)([0-9]+)$")
Creg = re.compile("^([A-Za-z0-9\.\+]+)\((\$[A-Za-z0-9]+)\)$")

def parse(flat):
    for ex in flat:
        if type(ex) == Instr:
            i = Instruction(ex)
            ex.gen = i.gen
            ex.need = i.need
            ex.c = i.c
            ex.label = i.label
            ex.ival = i.ival
    return flat

class Instruction(object):

    def __init__(self,ins):
        self.type = None
        self.ins = ins
        self.gen = []
        self.need = []
        self.c = None
        self.label = None
        self.ival = None
        self.parse(self.ins)

    def __str__(self):
        string  = ""
        if self.type:
            string += self.type
        if self.need:
            string += " Needs: " + str(self.need)
        if self.gen:
            string += ". Gens: " + str(self.gen)
            
        if self.label:
            string += ". Label: " + str(self.label)
        if self.ival:
            string += ". iVal: " + str(self.ival)
        if self.c:
            string += ". Offset: " + str(self.c)        
        return string
    
    def parse(self, ins):
        """
        Parses the instruction, to determine wich registers are used and set. 
        It also sets the offset used for loading an storing, used labels and
        used immidiate values.
        """
        if type(ins)!=Instr:
            raise Exception("You are parsing object that isn't a instruction")
        self.type = ins.instr
        if ins.instr in control_instructions:
            self.parse_control(ins)
        elif ins.instr in loadstore_instructions:
            self.parse_ls(ins)            
        elif ins.instr in intarithm_instructions :
            self.parse_int(ins)
        elif ins.instr in floatarithm_instructions:
            self.parse_float(ins)
        elif ins.instr in misc_instructions:
            self.parse_misc(ins)
        else:
            self.parse_unknown(ins)

    def parse_control(self,ins):
        """
        Parses the control type instructions.
        """    
        if ins.instr == 'j':
            if len(ins.args) == 1:
                if type(ins.args[0]) == Register:
                    self.need = [ins.args[0]]
                    if ins.args[0].expr == "$31":
                        self.need += [Register("$2"), Register("$3"),Register("$16"),Register("$17"),Register("$18"),Register("$19"),Register("$20"),Register("$21"),Register("$22"),Register("$23"),Register("$f0"),Register("$f1"),Register("$f2"),Register("$f3"),Register("$fp"),Register("$sp"),Register("$f20"),Register("$f22"),Register("$f24"),Register("$f26"),Register("$f28"),Register("$f30")]
                else:
                    self.label = [ins.args[0]]
                
                
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
        
        elif ins.instr == 'jal':
            self.gen = [Register("$31"),Register("$2"),Register("$3"),Register("$f0")] #Return address and values
            #Reg $4,5,6,7 are registers that are used for fuction arguments.
            # $f12, $f13, $f14, $f15 parameter registers zijn voor functies. 
            # http://msdn.microsoft.com/en-us/library/ms253512%28v=vs.90%29.aspx            
            #it is not clear which one will be used.
            self.need = [Register("$4"),Register("$5"),Register("$6"),Register("$7"),Register("$fp"), Register("$sp"),Register("$f12"),Register("$f13"),Register("$f14"),Register("$f15")]
            
        elif ins.instr == 'jr':
            if len(ins.args) == 1:
                self.need = [ins.args[0]]
                if ins.args[0].expr == "$31":
                    self.need += [Register("$2"), Register("$3"),Register("$16"),Register("$17"),Register("$18"),Register("$19"),Register("$20"),Register("$21"),Register("$22"),Register("$23"),Register("$f0"),Register("$f1"),Register("$f2"),Register("$f3"),Register("$fp"),Register("$sp"),Register("$f20"),Register("$f22"),Register("$f24"),Register("$f26"),Register("$f28"),Register("$f30")]     
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
            
        elif ins.instr == 'jalr':
            if len(ins.args) == 1:
                #Reg $4,5,6,7 are registers that are used for fuction arguments.
                # $f12, $f13, $f14, $f15 parameter registers zijn voor functies. 
                # http://msdn.microsoft.com/en-us/library/ms253512%28v=vs.90%29.aspx
                #it is not clear which one will be used.
                self.need = [ins.args[0],Register("$4"),Register("$5"),Register("$6"),Register("$7"),Register("$fp"), Register("$sp"),Register("$f12"),Register("$f13"),Register("$f14"),Register("$f15")]
                self.gen = [Register("$2"),Register("$3"),Register("$f0")] #Return values
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
            
        elif ins.instr == 'beq':
            if len(ins.args) == 3:
                self.need = [ins.args[0],ins.args[1]]
                self.label = Label(ins.args[2])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                           
        elif ins.instr == 'bne':
            if len(ins.args) == 3:
                self.need = [ins.args[0],ins.args[1]]
                self.label = Label(ins.args[2])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'blez':
            if len(ins.args) == 2:
                self.need = [ins.args[0]]
                self.label = Label(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bgtz':
            if len(ins.args) == 2:
                self.need = [ins.args[0]]
                self.label = Label(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bltz':
            if len(ins.args) == 2:
                self.need = [ins.args[0]]
                self.label = Label(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bgez':
            if len(ins.args) == 2:
                self.need = [ins.args[0]]
                self.label = Label(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bct':
            if len(ins.args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bcf':
            if len(ins.args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bc1f':
            if len(ins.args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'bc1t':
            if len(ins.args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)


    def parse_ls(self,ins):
        """
        Parses the load/store type instructions.
        """
        global Creg
        if ins.instr == 'lb':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                       
        elif ins.instr == 'lbu':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                 
        elif ins.instr == 'lh':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'lhu':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'lw':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                 
        elif ins.instr == 'dlw':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.gen = self.double_reg(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                 
        elif ins.instr == 'dmfc1':
            if len(ins.args) == 2:
                self.need = [ins.args[1]] 
                self.gen = self.double_reg(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'l.s':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'l.d':
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'sb':   
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.need = [ins.args[0]] + self.need                    
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                  
        elif ins.instr == 'sbu':  
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.need = [ins.args[0]] + self.need                    
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                       
        elif ins.instr == 'sh':   
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.need = [ins.args[0]] + self.need                    
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                       
        elif ins.instr == 'shu':  
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.need = [ins.args[0]] + self.need                    
                    
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                        
        elif ins.instr == 'sw':   
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.need = [ins.args[0]] + self.need
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                      
        elif ins.instr == 'dsw':  
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.need = self.double_reg(ins.args[0]) + self.need                    
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                     
        elif ins.instr == 'dsz':  
            if len(ins.args) == 1:
                g = re.match(Creg, ins.args[0])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[0]]  
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                    
        elif ins.instr == 's.s':  
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]]
                self.need = [ins.args[0]] + self.need                    
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                         
        elif ins.instr == 's.d':  
            if len(ins.args) == 2:
                g = re.match(Creg, ins.args[1])
                if g:
                    self.c = g.group(1)
                    self.need = [Register(g.group(2))]
                else:
                    self.need = [ins.args[1]] 
                self.need = self.double_reg(ins.args[0]) + self.need                        
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                                      
        elif ins.instr == 'move':
            if len(ins.args) == 2:
                self.need = [ins.args[1]]
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                         
        elif ins.instr == 'mov.d':
            if len(ins.args) == 2:
                self.need = self.double_reg(ins.args[1])
                self.gen = self.double_reg(ins.args[0])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                         
        elif ins.instr == 'mov.s':
            if len(ins.args) == 2:
                self.need = [ins.args[1]]
                self.gen = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                         
        elif ins.instr == 'li':
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.ival = ins.args[1]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
            

    def parse_int(self,ins):
        """
        Parses the int type instructions.
        """
        if ins.instr == 'add':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                         
        elif ins.instr == 'addi': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
        
        elif ins.instr == 'addu': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
        elif ins.instr == 'addiu':
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                        
        elif ins.instr == 'sub': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                         
        elif ins.instr == 'subu': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'mult': 
            if len(ins.args) == 2:
                self.gen = [Register("$hi"),Register("$lo")]
                self.need = [ins.args[0], ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                      
        elif ins.instr == 'multu':
            if len(ins.args) == 2:
                self.gen = [Register("$hi"),Register("$lo")]
                self.need = [ins.args[0], ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                        
        elif ins.instr == 'div':  
            if len(ins.args) == 2:
                self.gen = [Register("$hi"),Register("$lo")]
                self.need = [ins.args[0], ins.args[1]]
            elif len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1], ins.args[2]]                
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                        
        elif ins.instr == 'divu': 
            if len(ins.args) == 2:
                self.gen = [Register("$hi"),Register("$lo")]
                self.need = [ins.args[0], ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)   
                        
        elif ins.instr == 'and': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                         
        elif ins.instr == 'andi': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
                
        elif ins.instr == 'or':   
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'ori':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
                
        elif ins.instr == 'xor':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                         
        elif ins.instr == 'xori': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
                
        elif ins.instr == 'nor':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                                
        elif ins.instr == 'sll':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'sllv': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'srl':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'srlv': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'sra':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'srav': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'slt':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'slti': 
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
                
        elif ins.instr == 'sltu':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                if self.is_reg(ins.args[2]):
                    self.need = [ins.args[1], ins.args[2]]
                else: 
                    self.need = [ins.args[1]]
                    self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)        
                  
        elif ins.instr == 'sltiu':
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
                self.ival = ins.args[2]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)           
   

    def parse_float(self,ins):
        """
        Parses the float type instructions.
        """
        if ins.instr == 'add.s':   
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1], ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                        
        elif ins.instr == 'add.d':   
            if len(ins.args) == 3:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1]) + self.double_reg(ins.args[2])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'sub.s':   
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1], ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'sub.d':  
            if len(ins.args) == 3:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1]) + self.double_reg(ins.args[2])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'mul.s':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1], ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'mul.d':  
            if len(ins.args) == 3:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1]) + self.double_reg(ins.args[2])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'div.s':  
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1], ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'div.d': 
            if len(ins.args) == 3:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1]) + self.double_reg(ins.args[2])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                         
        elif ins.instr == 'abs.s':  
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                 
        elif ins.instr == 'abs.d':  
            if len(ins.args) == 2:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'neg.s':  
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'neg.d':  
            if len(ins.args) == 2:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'sqrt.s': 
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'sqrt.d': 
            if len(ins.args) == 2:
                self.gen = self.double_reg(ins.args[0])
                self.need = self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt':    
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt.d.w':
            if len(ins.args) == 2:
                self.gen = self.double_reg(ins.args[0])
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt.s.d':
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt.d.s':
            if len(ins.args) == 2:
                self.gen = self.double_reg(ins.args[0])
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt.s.w':
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt.w.s':
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'cvt.w.d':
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'c.eq.s': 
            if len(ins.args) == 2:
                self.gen = [Register("$fcc")]
                self.need = [ins.args[0],ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                                      
        elif ins.instr == 'c.eq.d': 
            if len(ins.args) == 2:
                self.gen = [Register("$fcc")]
                self.need = self.double_reg(ins.args[0]) + self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'c.lt.s': 
            if len(ins.args) == 2:
                self.gen = [Register("$fcc")]
                self.need = [ins.args[0],ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                         
        elif ins.instr == 'c.lt.d': 
            if len(ins.args) == 2:
                self.gen = [Register("$fcc")]
                self.need = self.double_reg(ins.args[0]) + self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                         
        elif ins.instr == 'c.le.s': 
            if len(ins.args) == 2:
                self.gen = [Register("$fcc")]
                self.need = [ins.args[0],ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                         
        elif ins.instr == 'c.le.d': 
            if len(ins.args) == 2:
                self.gen = [Register("$fcc")]
                self.need = self.double_reg(ins.args[0]) + self.double_reg(ins.args[1])
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                         
        elif ins.instr == 'trunc.l.d':
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = self.double_reg(ins.args[1]) + [ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                         
        elif ins.instr == 'trunc.l.s':
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1],ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                        
        elif ins.instr == 'trunc.w.d':
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = self.double_reg(ins.args[1]) + [ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
        
        elif ins.instr == 'trunc.w.s':
            if len(ins.args) == 3:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1],ins.args[2]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)        
            

    def parse_misc(self,ins):
        """
        Parses the misc type instructions.
        """
        if ins.instr == 'nop':
            if len(ins.args) != 0:
                raise Exception("Invalid number of args for ins: ", ins.instr)
        elif ins.instr == 'syscall':
            if len(ins.args) != 0:
                raise Exception("Invalid number of args for ins: ", ins.instr)
        elif ins.instr == 'break':
            if len(ins.args) != 0:
                raise Exception("Invalid number of args for ins: ", ins.instr)
        elif ins.instr == 'mflo': 
            if len(ins.args) == 1:
                self.gen = [ins.args[0]]
                self.need = [Register("$lo")]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                
        elif ins.instr == 'mtlo':  
            if len(ins.args) == 1:
                self.gen = [Register("$lo")]
                self.need = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                           
        elif ins.instr == 'mfhi':   
            if len(ins.args) == 1:
                self.gen = [ins.args[0]]
                self.need = [Register("$hi")]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                         
        elif ins.instr == 'mthi':     
            if len(ins.args) == 1:
                self.gen = [Register("$hi")]
                self.need = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                          
        elif ins.instr == 'mtc1':    
            if len(ins.args) == 2:
                self.gen = [ins.args[1]]
                self.need = [ins.args[0]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)  
                       
        elif ins.instr == 'mfc1':  
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.need = [ins.args[1]]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr) 
                           
        elif ins.instr == 'la':   
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.ival = ins.args[1]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)
                            
        elif ins.instr == 'lui':        
            if len(ins.args) == 2:
                self.gen = [ins.args[0]]
                self.ival = ins.args[1]
            else:
                raise Exception("Invalid number of args for ins: ", ins.instr)        

    def parse_unknown(self,ins):
        """
        As we scanned all files were we will run benchmarks on, we will not
        encounter any unknown instructions for this assignment. This function
        is for later.
        """
        raise Exception("Unknown instruction type: ", ins.instr)
        
    def double_reg(self, reg):
        """
        Return two registers in a list: the one that is given as an argument
        and the one that comes after it (numrical).
        This is for float operations with double precision.
        """
        global numreg
        if type(reg) != Register:
            raise Exception("Not a register object")
        g = re.match(numreg, reg.expr)
        return [reg, Register(g.group(1) + str(int(g.group(2)) + 1))]
        
    def is_reg(self, val):
        return type(val) == Register 

def main():
    # test code
    from asmyacc import parser

    flat = []
    for line in open('../benchmarks/whet.s', 'r').readlines():
        if not line.strip(): continue
        flat.append(parser.parse(line))
        
    for inst in flat:
        if type(inst)==Instr:
            try:
                Instruction(inst)
            except Exception as e:
                print inst.instr, inst.args
                raise e
            
if __name__ == '__main__':
    main()
    pass
