# ------------------------------------------------------------
# asmyacc.py
#
# assembly parser
#
# Run this module without arguments to use the interative
# parser. Give a filename as argument to parse a file.
# ------------------------------------------------------------

import yacc
from ir import *
import sys

# Get the token map from the lexer.  This is required.
from asmlex import tokens

raise_on_error = False

def p_expr(p):
    '''expr : raw
            | label
            | comment
            | instr
            | instr comment
            '''
    p[0] = p[1]


def p_raw(p):
    'raw : RAW'
    p[0] = Raw(p[1])


def p_label(p):
    '''label : ID ':' '''
    p[0] = Label(p[1])


def p_comment(p):
    'comment : COMMENT'
    p[0] = Comment(p[1])


# for nop
def p_instr_no_arg(p):
    '''instr : ID '''
    p[0] = Instr(p[1], [])


def p_instr_one_arg(p):
    '''instr : ID arg'''
    p[0] = Instr(p[1], [p[2]])


def p_instr_two_arg(p):
    '''instr : ID arg ',' arg'''
    p[0] = Instr(p[1], [p[2], p[4]])


def p_instr_three_arg(p):
    '''instr : ID arg ',' arg ',' arg'''
    p[0] = Instr(p[1], [p[2], p[4], p[6]])


# loop.17+4($3)

def p_arg(p):
    '''arg : int
           | hex
           | register
           | ID
           '''
    p[0] = p[1]


def p_arg_ext(p):
    '''arg : ID '+' arg
           | ID '-' arg
           '''
    p[0] = '%s%s%s' %(p[1],p[2],p[3])


def p_arg_brackets(p):
    '''arg : int '(' register ')'
           | ID  '(' register ')'
           '''
    p[0] = '%s(%s)' %(p[1], p[3].expr)


def p_int(p):
    'int : INT'
    p[0] = p[1]


def p_int_minus(p):
    '''int : '-' INT'''
    p[0] = -1*p[1]


def p_hex(p):
    'hex : HEX'
    p[0] = p[1]


def p_register(p):
    'register : REGISTER'
    p[0] = Register(p[1])


error_count = 0
# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    global raise_on_error
    global error_count
    error_count +=1
    if raise_on_error: raise Exception()


# Build the parser
parser = yacc.yacc()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        raise_on_error = True
        counter = 1
        for line in open(sys.argv[1], 'r').readlines():
           if not line.strip(): continue
           result = parser.parse(line)
           print counter, result
           counter +=1
           #if counter % 50 == 0: raw_input('pres key')
        print 'errors: %d\n' % error_count 

    else:
        while True:
           try:
               s = raw_input('asmyacc > ')
           except EOFError:
               break
           if not s: continue
           result = parser.parse(s)
           print repr(result)
