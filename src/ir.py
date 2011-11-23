#
# IR objects
#

control_instructions = [
    'j',     #- jump 
    'jal',   #- jump and link 
    'jr',    #- jump register 
    'jalr',  #- jump and link register 
    'beq',   #- branch == 0 
    'bne',   #- branch != 0 
    'blez',  #- branch <= 0 
    'bgtz',  #- branch > 0 
    'bltz',  #- branch < 0 
    'bgez',  #- branch >= 0 
    'bct',   #- branch FCC TRUE 
    'bcf'    #- branch FCC FALSE 
    ]

loadstore_instructions = [
    'lb',   #- load byte 
    'lbu',  #- load byte unsigned 
    'lh',   #- load half (short) 
    'lhu',  #- load half (short) unsigned 
    'lw',   #- load word 
    'dlw',  #- load double word 
    'l.s',  #- load single-precision FP 
    'l.d',  #- load double-precision FP 
    'sb',   #- store byte 
    'sbu',  #- store byte unsigned 
    'sh',   #- store half (short) 
    'shu',  #- store half (short) unsigned 
    'sw',   #- store word 
    'dsw',  #- store double word 
    's.s',  #- store single-precision FP 
    's.d',  #- store double-precision FP
    'move', # extra
    'li'
    ]

intarithm_instructions = [
    'add',  #- integer add 
    'addu', #- integer add unsigned 
    'sub',  #- subtract 
    'subu', #- integer subtract unsigned 
    'mult', #- integer multiply 
    'multu',#- integer multiply unsigned 
    'div',  #- integer divide 
    'divu', #- integer divide unsigned 
    'and',  #- logical AND 
    'or',   #- logical OR 
    'xor',  #- logical XOR 
    'nor',  #- logical NOR 
    'sll',  #- shift left logical 
    'srl',  #- shift right logical 
    'sra',  #- shift right arithmetic 
    'slt',  #- set less than 
    'sltu', #- set less than unsigned 
    ]

floatarithm_instructions = [
    'add.s',    #- single-precision (SP) add
    'add.d',    #- double-precision (DP) add
    'sub.s',    #- SP subtract
    'sub.d',    #- DP subtract
    'mult.s',   #- SP multiply
    'mult.d',   #- DP multiply
    'div.s',    #- SP divide
    'div.d',    #- DP divide
    'abs.s',    #- SP absolute value
    'abs.d',    #- DP absolute value
    'neg.s',    #- SP negation
    'neg.d',    #- DP negation
    'sqrt.s',   #- SP square root
    'sqrt.d',   #- DP square root
    'cvt',       #- int., single, double conversion
    'c.s',      #- SP compare
    'c.d',      #- DP compare
]

misc_instructions = [
    'nop',      #- no operation
    'syscall',  #- system call
    'break',    #- declare program error

    #extra
    'mflo',
    'mtcl',
    'la'
]



registers = [
    r'\$zero' #zero-valued source/sink
    r'\$at' #reserved by assembler
    r'\$v[0-1]', #fn return result regs
    r'\$a[0-3]', #fn argument value regs
    r'\$t[0-7]', #temp regs, caller saved
    r'\$s[0-7]', #saved regs, callee saved
    r'\$t[8-9]', #temp regs, caller saved
    r'\$k[0-1]', #reserved by OS
    r'\$gp', #global pointer
    r'\$sp', #stack pointer
    r'\$s8', #saved regs, callee saved
    r'\$ra', #return address reg
    r'\$hi', #high result register
    r'\$lo', #low result register
    r'\$f([1-2][0-9]|3[0-1]|[0-9])', #floating point registers $f0 - $f31
    r'\$fcc', #floating point condition code
    r'\$([1-2][0-9]|3[0-1]|[0-9])', #extra registers $0-$31 (not in spec! :s)
    r'\$fp',
    ]


class Expr(object):
    obtype = 'expr'
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return '<Expr %r>' % (self.expr,)

    def __str__(self):
        return self.expr

    def pattern(self):
        return self.obtype

class Instr(Expr):
    obtype = 'expr'
    def __init__(self, instr, args):
        self.instr = instr
        self.args = args

    def __repr__(self):
        return '<Instr %r %r>' % (self.instr, self.args)

    def __str__(self):
        return '%s ' % self.instr + ','.join((str(arg) for arg in self.args))

    def pattern(self):
        return '%s ' % self.instr + ','.join((arg.pattern() for arg in self.args))

class Register(Expr):
    obtype = 'reg'
    def __repr__(self):
        return '<Register %r>' % self.expr

class Raw(Expr):
    obtype = 'raw'
    def __repr__(self):
        return '<Raw %r>' % self.expr

        
class Comment(Expr):
    obtype = 'comment'
    def __repr__(self):
        return '<Comment %r>' % self.expr

class Label(Expr):
    obtype = 'label'
    def __repr__(self):
        return '<Label %r>' % self.expr

    def __str__(self):
        return '%s:' % self.expr