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
import math
from ply.lex import TOKEN

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME',
    'NUMBER',
    'COMMENT',
    'FLOAT',
    'SCIENTIFIC',
    'NONDECIMAL',
    'SALTO',
    'SIN',
    'EXP',
    'COS',
    'LOG'
)

literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens

t_NAME = r'(MEM_)(10|[1-9])'

t_COMMENT = r'%%.*'

t_SIN = r'sin'

t_EXP = r'exp'

t_COS = r'cos'

t_LOG = r'log'


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
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_SALTO(t):
    r'[\r\n]+'
    t.lexer.lineno += t.value.count("\n")
    return t


t_ignore = " \t"


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
    '''statement : expression 
                 | expression SALTO statement'''
    if p[1] is not None:
        print(p[1])


def p_statement_comment_2(p):
    'statement : COMMENT SALTO statement'
    pass


def p_statement_comment(p):
    'statement : COMMENT'
    pass


def p_expression_sin(p):
    "expression : SIN '(' expression ')'"
    p[0] = math.sin(p[3])


def p_expression_exp(p):
    "expression : EXP '(' expression ')'"
    p[0] = math.exp(p[3])


def p_expression_cos(p):
    "expression : COS '(' expression ')'"
    p[0] = math.cos(p[3])


def p_expression_log(p):
    "expression : LOG '(' expression ')'"
    p[0] = math.log(p[3])


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
    yacc.parse(f.read())
except IOError:
    print("Archivo no encontrado:", fname)
