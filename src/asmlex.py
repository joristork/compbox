# ------------------------------------------------------------
# asmlex.py
#
# assembly lexer
#
# Run this module without arguments to use the interative
# lexer. Give a filename as argument to tokenise a file.
# ------------------------------------------------------------

import lex
import sys

tokens = (
    'COMMENT',
    'RAW',
    'HEX',
    'INT',
    'REGISTER',
    'ID',
    )

def t_COMMENT(t):
    r'\#.*'
    return t

# We dont touch lines starting with '.'.
def t_RAW(t):
    r'\..+'
    return t

def t_HEX(t):
    r'0x[0-9a-f]+'
    return t

# Dont put '-' in regex. Yacc handles '-'.
def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# An ID token is either a label or an instruction.
def t_ID(t):
    r'(\$L){0,1}[_a-zA-Z0-9][_a-zA-Z0-9\.]*'
    return t

# Registers are expressions $[a-z0-9]+ .
def t_REGISTER(t):
    r'\$[a-z0-9]+'
    return t

literals = [ ',', '(', ')', ':', '.', '+', '-' ]

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

error_count = 0
# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    global error_count
    error_count += 1

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    # test
    if len(sys.argv) > 1:
        lex.input(''.join(open(sys.argv[1], 'r').readlines()))
        while 1:
            tok = lex.token()
            if not tok: break
            print tok
        print 'errors: %d\n' % error_count
    else:
        while True:
           try:
               s = raw_input('asmlex > ')
           except EOFError:
               break
           if not s: continue
           lex.input(s)
           while 1:
               tok = lex.token()
               if not tok: break
               print tok
           

