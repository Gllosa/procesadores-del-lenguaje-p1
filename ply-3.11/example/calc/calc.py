# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import os
import ply.yacc as yacc
import ply.lex as lex
import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME', 'NUMBER', 'COMMENT', 'FLOAT', 'SCIENTIFIC', 'NONDECIMAL'
)

literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_COMMENT = r'%%.*\n'


def t_NONDECIMAL(t):
    r'[0][O|o|X|x]\d+'
    if t.value[1] == "O" or t.value[1] == "o":
        t.value = int(t.value[2:len(t.value)], 8)
    else:
        t.value = int(t.value[2:len(t.value)], 16)
    return t


def t_SCIENTIFIC(t):
    r'[+-]?([0-9]*[.])?[0-9]+[e][+-]?([0-9]*[.])?[0-9]+'
    t.value = float(t.value)
    return t


def t_FLOAT(t):
    r'[+-]?([0-9]*[.])?[0-9]+'
    # if t.value[0] == '.':
    #    t.value = float('0.' + t.value[1:-1])
    #    return t
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression '
    if p[1] is not None:
        print(p[1])


def p_statement_comment(p):
    'statement : COMMENT'
    pass


def p_expression_comment(p):
    'expression : COMMENT'
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uplus(p):
    "expression : '+' expression"
    p[0] = p[2]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_scientific(p):
    "expression : SCIENTIFIC"
    p[0] = p[1]


def p_expression_float(p):
    "expression : FLOAT"
    p[0] = p[1]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_nondecimal(p):
    "expression : NONDECIMAL"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_expression_comment_same_line(p):
    "expression : expression COMMENT"
    print(p[1])


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
fname = "\input.txt"

try:
    f = open(ROOT_DIR + fname, 'r')
    lines = ''.join(f.readlines())
    print(lines)
    yacc.parse(f.read())
except IOError:
    print("Archivo no encontrado:", fname)

# while 1:
#     try:
#         s = f.readline()
#     except EOFError:
#         break
#     if not s:
#         break
#     yacc.parse(s)
