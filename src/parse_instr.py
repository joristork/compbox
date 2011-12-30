from ir import *
import re

class Instruction(object):
    
    def __init__(self,ins):
        self.Creg = re.compile("^([0-9]+)\((\$[A-Za-z0-9]+)\)$")
        self.type = None
        self.ins = ins
        self.gen = None
        self.need = []
        self.c = None
        self.label = None
        self.parse(self.ins)
        
    def parse(self, ins):
        if type(ins)!=Instr:
            raise Exception("You are parsing object that isn't a instruction")
        self.type = ins.instr
        if ins.instr in control_instructions:
            self.gen,self.need,self.c = self.parse_control(ins)
        elif ins.instr in loadstore_instructions:
            self.gen,self.need,self.c = self.parse_ls(ins)            
        elif ins.instr in intarithm_instructions :
            self.gen,self.need,self.c = self.parse_int(ins)
        elif ins.instr in floatarithm_instructions:
            self.gen,self.need,self.c = self.parse_float(ins)
        elif ins.instr in misc_instructions:
            self.gen,self.need,self.c = self.parse_misc(ins)
        else:
            self.gen,self.need,self.c = self.parse_unknown(ins)

    def parse_control(self,ins):
        gen,need,c = (None,[],None) 
        if ins.instr == 'j':
            pass
        
        elif ins.instr == 'jal':
            self.gen = Register("$31") #Return address
            
        elif ins.instr == 'jr':
            if len(args) == 1:
                self.need = [args[0]]
            else:
                raise Exception("Invalid number of args")
            
        elif ins.instr == 'jalr':
            if len(args) == 1:
                self.need = [args[0]]
                self.gen = Register("$31") #Return address
            else:
                raise Exception("Invalid number of args")
            
        elif ins.instr == 'beq':
            if len(args) == 3:
                self.need = [args[0],args[1]]
                self.label = Label(args[2])
            else:
                raise Exception("Invalid number of args")            
        elif ins.instr == 'bne':
            if len(args) == 3:
                self.need = [args[0],args[1]]
                self.label = Label(args[2])
            else:
                raise Exception("Invalid number of args")               
        elif ins.instr == 'blez':
            if len(args) == 2:
                self.need = [args[0]]
                self.label = Label(args[1])
            else:
                raise Exception("Invalid number of args")               
        elif ins.instr == 'bgtz':
            if len(args) == 2:
                self.need = [args[0]]
                self.label = Label(args[1])
            else:
                raise Exception("Invalid number of args")                 
        elif ins.instr == 'bltz':
            if len(args) == 2:
                self.need = [args[0]]
                self.label = Label(args[1])
            else:
                raise Exception("Invalid number of args")                 
        elif ins.instr == 'bgez':
            if len(args) == 2:
                self.need = [args[0]]
                self.label = Label(args[1])
            else:
                raise Exception("Invalid number of args")                 
        elif ins.instr == 'bct':
            if len(args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(args[0])
            else:
                raise Exception("Invalid number of args")                 
        elif ins.instr == 'bcf':
            if len(args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(args[0])
            else:
                raise Exception("Invalid number of args")               
        elif ins.instr == 'bc1f':
            if len(args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(args[0])
            else:
                raise Exception("Invalid number of args")               
        elif ins.instr == 'bc1t':
            if len(args) == 1:
                self.need = [Register("$fcc")]
                self.label = Label(args[0])
            else:
                raise Exception("Invalid number of args")               
            
        return gen, need, c

    def parse_ls(self,ins):
        gen,need,c = (None,[],None) 
        if ins.instr == 'lb':pass   
        elif ins.instr == 'lbu':pass  
        elif ins.instr == 'lh':pass   
        elif ins.instr == 'lhu':pass  
        elif ins.instr == 'lw':pass   
        elif ins.instr == 'dlw':pass  
        elif ins.instr == 'dmfc1':pass
        elif ins.instr == 'l.s':pass  
        elif ins.instr == 'l.d':pass  
        elif ins.instr == 'sb':pass   
        elif ins.instr == 'sbu':pass  
        elif ins.instr == 'sh':pass   
        elif ins.instr == 'shu':pass  
        elif ins.instr == 'sw':pass   
        elif ins.instr == 'dsw':pass  
        elif ins.instr == 'dsz':pass  
        elif ins.instr == 's.s':pass  
        elif ins.instr == 's.d':pass  
        elif ins.instr == 'move':pass 
        elif ins.instr == 'mov.d':pass
        elif ins.instr == 'mov.s':pass
        elif ins.instr == 'li':pass
            
        return gen, need, c
    
    def parse_int(self,ins):
        if ins.instr == 'add':pass  
        elif ins.instr == 'addi':pass 
        elif ins.instr == 'addu':pass 
        elif ins.instr == 'addiu':pass
        elif ins.instr == 'sub':pass  
        elif ins.instr == 'subu':pass 
        elif ins.instr == 'mult':pass 
        elif ins.instr == 'multu':pass
        elif ins.instr == 'div':pass  
        elif ins.instr == 'divu':pass 
        elif ins.instr == 'and':pass  
        elif ins.instr == 'andi':pass 
        elif ins.instr == 'or':pass   
        elif ins.instr == 'ori':pass  
        elif ins.instr == 'xor':pass  
        elif ins.instr == 'xori':pass 
        elif ins.instr == 'nor':pass  
        elif ins.instr == 'sll':pass  
        elif ins.instr == 'sllv':pass 
        elif ins.instr == 'srl':pass  
        elif ins.instr == 'srlv':pass 
        elif ins.instr == 'sra':pass  
        elif ins.instr == 'srav':pass 
        elif ins.instr == 'slt':pass  
        elif ins.instr == 'slti':pass 
        elif ins.instr == 'sltu':pass  
        elif ins.instr == 'sltiu':pass
            
        gen,need,c = (None,[],None) 
        
        return gen, need, c    

    def parse_float(self,ins):
        gen,need,c = (None,[],None) 
        if ins.instr == 'add.s':pass   
        elif ins.instr == 'add.d':pass   
        elif ins.instr == 'sub.s':pass   
        elif ins.instr == 'sub.d':pass  
        elif ins.instr == 'mul.s':pass  
        elif ins.instr == 'mul.d':pass  
        elif ins.instr == 'div.s':pass  
        elif ins.instr == 'div.d':pass  
        elif ins.instr == 'abs.s':pass  
        elif ins.instr == 'abs.d':pass  
        elif ins.instr == 'neg.s':pass  
        elif ins.instr == 'neg.d':pass  
        elif ins.instr == 'sqrt.s':pass 
        elif ins.instr == 'sqrt.d':pass 
        elif ins.instr == 'cvt':pass    
        elif ins.instr == 'cvt.d.w':pass
        elif ins.instr == 'cvt.s.d':pass
        elif ins.instr == 'cvt.d.s':pass
        elif ins.instr == 'cvt.s.w':pass
        elif ins.instr == 'cvt.w.s':pass
        elif ins.instr == 'cvt.w.d':pass
        elif ins.instr == 'c.eq.s':pass 
        elif ins.instr == 'c.eq.d':pass 
        elif ins.instr == 'c.lt.s':pass 
        elif ins.instr == 'c.lt.d':pass 
        elif ins.instr == 'c.le.s':pass 
        elif ins.instr == 'c.le.d':pass 
        elif ins.instr == 'trunc.l.d':pass
        elif ins.instr == 'trunc.l.s':pass
        elif ins.instr == 'trunc.w.d':pass
        elif ins.instr == 'trunc.w.s':pass
            
        return gen, need, c

    def parse_misc(self,ins):
        gen,need,c = (None,[],None) 
        if ins.instr == 'nop':pass      
        elif ins.instr == 'syscall':pass  
        elif ins.instr == 'break':pass    
        elif ins.instr == 'mflo':pass     
        elif ins.instr == 'mtlo':pass     
        elif ins.instr == 'mfhi':pass     
        elif ins.instr == 'mthi':pass     
        elif ins.instr == 'mtc1':pass     
        elif ins.instr == 'mfc1':pass     
        elif ins.instr == 'la':pass       
        elif ins.instr == 'lui':pass        
        return gen, need, c

    def parse_unknown(self,ins):
        """
        As we scanned all files were we will run benchmarks on, we will not
        encounter any unknown instructions for this assignment. This function
        is for later.
        """
        gen,need,c = (None,[],None) 
        raise Exception("Unknown instruction type: ", ins.instr)
        return gen, need, c    

def main():
    Instruction(Instr("beq",[]))
    
if __name__ == '__main__':
    main()
    pass
