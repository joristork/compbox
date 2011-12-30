#
# IR objects
#
# Reg $31 is a return register
control_instructions = [
    'j',     #- jump.                                                           Used: j {label}. Needs: [], Gen: [] 
    'jal',   #- jump and link.                                                  Used: jal {function}. Needs: [], Gen: [$31] 
    'jr',    #- jump register.                                                  Used: jr $x. Needs: [$x], Gen: [] 
    'jalr',  #- jump and link register.                                         Not used
    'beq',   #- branch == 0.                                                    Used: beq $a $b {label}. Needs: [$a,$b], Gen: [] 
    'bne',   #- branch != 0.                                                    Used: bne $a $b {label}. Needs: [$a,$b], Gen: []
    'blez',  #- branch <= 0.                                                    Used: blez $a {label}. Needs: [$a], Gen: []
    'bgtz',  #- branch > 0.                                                     Used: bgtz $a {label}. Needs: [$a], Gen: []
    'bltz',  #- branch < 0.                                                     Used: bltz $a {label}. Needs: [$a], Gen: []
    'bgez',  #- branch >= 0.                                                    Used: bgez $a {label}. Needs: [$a], Gen: [] 
    'bct',   #- branch FCC TRUE.                                                Used: bct {label}. Needs: [$fcc], Gen: [] 
    'bcf',   #- branch FCC FALSE.                                               Used: bcf {label}. Needs: [$fcc], Gen: [] 
    'bc1f',  #- Branch on floating point compare false.                         Used: bc1t {label}. Needs: [$fcc], Gen: [] 
    'bc1t'   #- Branch on floating point compare true.                          Used: bc1t {label}. Needs: [$fcc], Gen: [] 
    ]

loadstore_instructions = [
    'lb',   #- load byte.                                                       Used: lb $a C($b). Needs: [$b], Gen: [$a] 
    'lbu',  #- load byte unsigned.                                              Used: lbu $a C($b). Needs: [$b], Gen: [$a] 
    'lh',   #- load half (short).                                               Used: lh $a C($b). Needs: [$b], Gen: [$a] 
    'lhu',  #- load half (short) unsigned.                                      Used: lhu $a C($b). Needs: [$b], Gen: [$a] 
    'lw',   #- load word.                                                       Used: lw $a C($b). Needs: [$b], Gen: [$a] 
    'dlw',  #- load double word .                                               Used: dlw $a C($b). Needs: [$b], Gen: [$a, $(a+1)] 
    'dmfc1',#- Doubleword move from floating point.                             Used: dmfc1 $a $b. Needs: [$b], Gen: [$a, $(a+1)]
    'l.s',  #- load single-precision FP.                                        Used: l.s $a C($b). Needs: [$b], Gen: [$a] 
    'l.d',  #- load double-precision FP.                                        Used: l.d $a C($b). Needs: [$b], Gen: [$a, $(a+1)]  
    'sb',   #- store byte.                                                      Used: sb $a C($b). Needs: [$a,$b], Gen: [] 
    'sbu',  #- store byte unsigned.                                             Used: sbu $a C($b). Needs: [$a,$b], Gen: [] 
    'sh',   #- store half (short).                                              Used: sh $a C($b). Needs: [$a,$b], Gen: [] 
    'shu',  #- store half (short) unsigned.                                     Used: shu $a C($b). Needs: [$a,$b], Gen: [] 
    'sw',   #- store word.                                                      Used: sw $a C($b). Needs: [$a,$b], Gen: [] 
    'dsw',  #- store double word.                                               Used: dsw $a C($b). Needs: [$b,$a, $(a+1)], Gen: [] 
    'dsz',  #- Double store zero.                                               Used: dsz C($a). Needs: [$a], Gen: [] 
    's.s',  #- store single-precision FP.                                       Used: s.s $a C($b). Needs: [$a,$b], Gen: [] 
    's.d',  #- store double-precision FP.                                       Used: s.d $a C($b). Needs: [$a, $(a+1),$b], Gen: [] 
    'move', #- Move register value.                                             Used: move $a $b. Used: move $a $b. Needs: [$b], Gen: [$a]
    'mov.d',#- Move floating point value. mov.d $a $b.                          Used: mov.d $a $b. Needs: [$b, $(b+1)], Gen: [$a, $(a+1)]
    'mov.s',#- Move floating point value. mov.s $a $b.                          Used: mov.s $a $b. Needs: [$b], Gen: [$a]    
    'li'    #- Load immidiate.                                                  Used: li $a {val}. Needs: [], Gen: [$a] 
    ]

intarithm_instructions = [
    'add',  #- integer add.                                                     Used: add $a $b $c or add $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'addi', #- integer add.                                                     Used: addi $a $b val. Needs: [$b], Gen: [$a] 
    'addu', #- integer add unsigned.                                            Used: addu $a $b $c or addu $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'addiu',#- integer add.                                                     Used: addiu $a $b val. Needs: [$b], Gen: [$a] 
    'sub',  #- subtract.                                                        Used: sub $a $b $c or sub $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'subu', #- integer subtract unsigned.                                       Used: subu $a $b $c or subu $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'mult', #- integer multiply.                                                Used: mult $a $b . Needs: [$a,$b], Gen: [$hi,$lo] 
    'multu',#- integer multiply unsigned.                                       Used: multu $a $b . Needs: [$a,$b], Gen: [$hi,$lo] 
    'div',  #- integer divide.                                                  Used: div $a $b . Needs: [$a,$b], Gen: [$hi,$lo] 
    'divu', #- integer divide unsigned.                                         Used: div $a $b . Needs: [$a,$b], Gen: [$hi,$lo] 
    'and',  #- logical AND.                                                     Used: and $a $b $c or and $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'andi', #- logical AND.                                                     Used: andi $a $b val. Needs: [$b], Gen: [$a] 
    'or',   #- logical OR.                                                      Used: or $a $b $c or or $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'ori',  #- logical OR.                                                      Used: ori $a $b val. Needs: [$b], Gen: [$a]
    'xor',  #- logical XOR.                                                     Used: xor $a $b $c or xor $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'xori', #- logical XOR.                                                     Used: xori $a $b val. Needs: [$b], Gen: [$a]
    'nor',  #- logical NOR.                                                     Used: nor $a $b $c. Needs: [$b,$c], Gen: [$a] 
    'sll',  #- shift left logical.                                              Used: sll $a $b {val}. Needs: [$b], Gen: [$a] 
    'sllv', #- Not used, but in user guide.                                     Used: sllv $a $b {val}. Needs: [$b], Gen: [$a] 
    'srl',  #- shift right logical.                                             Used: srl $a $b {val}. Needs: [$b], Gen: [$a] 
    'srlv', #- Not used, but in user guide.                                     Used: srlv $a $b {val}. Needs: [$b], Gen: [$a] 
    'sra',  #- shift right arithmetic.                                          Used: sra $a $b {val}. Needs: [$b], Gen: [$a] 
    'srav', #- Not used, but in user guide.                                     Used: srav $a $b {val}. Needs: [$b], Gen: [$a] 
    'slt',  #- set less than.                                                   Used: slt $a $b $c or slt $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'slti', #- set less than.                                                   Used: slti $a $b val. Needs: [$b], Gen: [$a]
    'sltu', #- set less than unsigned.                                          Used: sltu $a $b $c or sltu $a $b val. Needs: [$b(,$c)], Gen: [$a] 
    'sltiu' #- set less than unsigned.                                          Used: sltiu $a $b val. Needs: [$b], Gen: [$a]
    ]

floatarithm_instructions = [
    'add.s',    #- single-precision (SP) add.                                   Used: add.s $a $b $c. Needs: [$b,$c], Gen: [$a] 
    'add.d',    #- double-precision (DP) add.                                   Used: add.d $a $b $c. Needs: [$b, $(b+1),$c, $(c+1)], Gen: [$a, $(a+1)] 
    'sub.s',    #- SP subtract.                                                 Used: sub.s $a $b $c. Needs: [$b,$c], Gen: [$a] 
    'sub.d',    #- DP subtract.                                                 Used: sub.d $a $b $c. Needs: [$b, $(b+1),$c, $(c+1)], Gen: [$a, $(a+1)]
    'mul.s',    #- SP multiply.                                                 Used: mul.s $a $b $c. Needs: [$b,$c], Gen: [$a] 
    'mul.d',    #- DP multiply.                                                 Used: mul.d $a $b $c. Needs: [$b, $(b+1),$c, $(c+1)], Gen: [$a, $(a+1)]
    'div.s',    #- SP divide.                                                   Used: div.s $a $b $c. Needs: [$b,$c], Gen: [$a] 
    'div.d',    #- DP divide.                                                   Used: div.d $a $b $c. Needs: [$b, $(b+1),$c, $(c+1)], Gen: [$a, $(a+1)]
    'abs.s',    #- SP absolute value.                                           Used: abs.s $a $b. Needs: [$b], Gen: [$a]
    'abs.d',    #- DP absolute value.                                           Used: abs.d $a $b. Needs: [$b, $(b+1)], Gen: [$a, $(a+1)]
    'neg.s',    #- SP negation.                                                 Used: neg.s $a $b. Needs: [$b], Gen: [$a]
    'neg.d',    #- DP negation.                                                 Used: neg.d $a $b. Needs: [$b, $(b+1)], Gen: [$a, $(a+1)]
    'sqrt.s',   #- SP square root.                                              Used: sqrt.s $a $b. Needs: [$b], Gen: [$a]
    'sqrt.d',   #- DP square root.                                              Used: sqrt.d $a $b. Needs: [$b, $(b+1)], Gen: [$a, $(a+1)]
    'cvt',      #- int., single, double conversion.                             Used: cvt $a $b. Needs: [$b], Gen: [$a]
    'cvt.d.w',  #- Integer to float.                                            Used: cvt.d.w $a $b. Needs: [$b], Gen: [$a, $(a+1)]
    'cvt.s.d',  #- Float: double to single precision.                           Used: cvt.s.d $a $b. Needs: [$b, $(b+1)], Gen: [$a]
    'cvt.d.s',  #- Float: single to double precision.                           Used: cvt.d.s $a $b. Needs: [$b], Gen: [$a, $(a+1)]        
    'cvt.s.w',  #- Float: integer to single precision.                          Used: cvt.s.w $a $b. Needs: [$b], Gen: [$a]    
    'cvt.w.s',  #- Float: single precision to integer.                          Used: cvt.w.s $a $b. Needs: [$b], Gen: [$a]
    'cvt.w.d',  #- Float: double precision to integer.                          Used: cvt.w.d $a $b. Needs: [$b, $(b+1)], Gen: [$a]        
    'c.eq.s',   #- SP compare.                                                  Used: c.eq.s $a $b. Needs: [$a, $(a+1),$b, $(b+1)], Gen: [$fcc]
    'c.eq.d',   #- DP compare.                                                  Used: c.eq.d $a $b. Needs: [$a,$b], Gen: [$fcc]
    'c.lt.s',   #- SP compare.                                                  Used: c.lt.s $a $b. Needs: [$a,$b], Gen: [$fcc]
    'c.lt.d',   #- DP compare.                                                  Used: c.lt.d $a $b. Needs: [$a, $(a+1),$b, $(b+1)], Gen: [$fcc]
    'c.le.s',   #- SP compare.                                                  Used: c.le.s $a $b. Needs: [$a,$b], Gen: [$fcc]
    'c.le.d',   #- DP compare.                                                  Used: c.le.d $a $b. Needs: [$a, $(a+1),$b, $(b+1)], Gen: [$fcc]  
    'trunc.l.d',#- Convert FP.                                                  Used: trunc.l.d $a $b $c. Needs: [$b, $(b+1),$c], Gen:[$a]       
    'trunc.l.s',#- Convert FP.                                                  Used: trunc.l.s $a $b $c. Needs: [$b,$c], Gen: [$a] 
    'trunc.w.d',#- Convert FP.                                                  Used: trunc.w.d $a $b $c. Needs: [$b, $(b+1),$c], Gen:[$a] 
    'trunc.w.s' #- Convert FP.                                                  Used: trunc.w.s $a $b $c. Needs: [$b,$c], Gen: [$a]              
]

misc_instructions = [
    'nop',      #- no operation.                                                Used: nop
    'syscall',  #- system call,                                                 Used: syscall
    'break',    #- declare program error.                                       Used: break

    #extra
    'mflo',     #- Move from lo.                                                Used: mflo $a. Needs: [$lo], Gen: [$a]
    'mtlo',     #- Move to lo.                                                  Used: mtlo $a. Needs: [$a], Gen: [$lo]
    'mfhi',     #- Move from hi.                                                Used: mfhi $a. Needs: [$hi], Gen: [$a]
    'mthi',     #- Move to hi.                                                  Used: mthi $a. Needs: [$a], Gen: [$hi]
    'mtc1',     #- From int reg to float reg.                                   Used: mtc1 $a $b. Needs: [$a], Gen: [$b]
    'mfc1',     #- From float reg to int reg.                                   Used: mfc1 $a $b. Needs: [$b], Gen: [$a]
    'la',       #- Load address.                                                Used: la $a {label}. Needs: [], Gen: [$a]
    'lui'       #- Load upper immidiate:                                        Used: lui $a {val}. Needs: [], Gen: [$a]
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
    r'\$fp' #Frame pointer
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
    obtype = 'instr'
    
    def __init__(self, instr, args):
        self.instr = instr
        self.args = args
        self.gen = []
        self.need = []
        self.c = None
        self.label = None
        self.ival = None

    def jump_dest(self):
        if self.instr in control_instructions:
            return self.args[-1]
        else:
            raise Exception('this is not a jump/branch')

    def __repr__(self):
        return '<Instr %r %r>' % (self.instr, self.args)

    def __str__(self):
        return '\t%s\t' % self.instr + ','.join((str(arg) for arg in self.args))

    def pattern(self):
        return '%s\t' % self.instr + ','.join((arg.pattern() for arg in self.args))

class Register(Expr):
    obtype = 'reg'
    def __repr__(self):
        return '<Register %r>' % self.expr

class Raw(Expr):
    obtype = 'raw'
    def __repr__(self):
        return '<Raw %r>' % self.expr
    def __str__(self):
        return '\t%s' % self.expr

        
class Comment(Expr):
    obtype = 'comment'
    def __repr__(self):
        return '<Comment %r>' % self.expr
    def __str__(self):
        return '\t%s' % self.expr


class Label(Expr):
    obtype = 'label'
    def __repr__(self):
        return '<Label %r>' % self.expr

    def __str__(self):
        return '%s:' % self.expr
