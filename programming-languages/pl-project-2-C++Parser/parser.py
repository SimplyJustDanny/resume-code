import logging
import ply.lex as lex
import ply.yacc as yacc

# Keywords for easy conversion of regex to tokens
keywords = {
    'if' : 'IF', 'else' : 'ELSE', 'while' : 'WHILE', 'let' : 'LET',
    'loop' : 'LOOP', 'fn' : 'FN', 'mut' : 'MUT', 'ref' : 'REF', 'in' : 'IN',
    'struct' : 'STRUCT', 'type' : 'TYPE', 'return' : 'RETURN', 'true' : 'TRUE',
    'false' : 'FALSE', 'where' : 'WHERE', 'write' : 'WRITE', 'int' : 'INT',
    'float' : 'FLOAT', 'çhar' : 'CHAR', 'str': 'STR', 'boolean' : 'BOOLEAN',
}

tokens = [
    'IDENTIFIER', 'NUMBER',
    # Delimiters
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'LSQR', 'RSQR', 'SEMICOLON', 
    'COMMA',
    # Operators
    'EQUALS', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT', 'PLUS', 'MINUS', 'STAR', 
    'SLASH', 'MOD',
] + list(set(keywords.values()))

# Make sure operations retain a specific order to remove ambiguity
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH'),
    ('left', 'EQUALS', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT'),
)

# Handlers that ignore whitespace, comments, newlines,
# and print illegal chars respectively
t_ignore = ' \t'

def t_ignore_comment(t):
    r'//.*|/\*[\w\W]*\*/'
    pass

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Regular expression rules for simple tokens
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LSQR      = r'\['
t_RSQR      = r'\]'
t_SEMICOLON = r';'
t_COMMA     = r','

t_EQUALS    = r'='
t_NEQ       = r'!='
t_LEQ       = r'<='
t_GEQ       = r'>='
t_LT        = r'<'
t_GT        = r'>'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_STAR      = r'\*'
t_SLASH     = r'/'
t_MOD       = r'%'

# Regular expression for identifiers, which parses keywords in the token list
def t_IDENTIFIER(t):
    r'[a-z_][a-z_0-9]*'
    if t.value in keywords.keys():
        t.type = keywords[t.value]
    return t

# Regular expression for numbers, which are then parsed as ints
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Define the parser functions
def p_program(p):
    """program : statements"""
    pass

def p_statements(p):
    """statements : statement
                  | statements statement"""
    pass

def p_statement(p):
    """statement : assignment_statement
                 | if_statement
                 | if_else_statement
                 | while_statement
                 | action_statement
                 | let_expression                 
                 | function
                 | struct"""
    pass

def p_assignment_statement(p):
    """assignment_statement : let_expression EQUALS expression SEMICOLON
                            | IDENTIFIER EQUALS expression SEMICOLON"""
    pass

def p_if_statement(p):
    """if_statement : IF LPAREN expression RPAREN LCURLY statements RCURLY"""
    pass

def p_if_else_statement(p):
    """if_else_statement : IF LPAREN expression RPAREN LCURLY statements RCURLY ELSE LCURLY statements RCURLY
                         | IF LPAREN expression RPAREN LCURLY statements RCURLY ELSE if_statement
                         | IF LPAREN expression RPAREN LCURLY statements RCURLY ELSE if_statement ELSE LCURLY statements RCURLY"""
    pass

def p_while_statement(p):
    """while_statement : WHILE LPAREN expression RPAREN LCURLY statements RCURLY"""
    pass

def p_action_statement(p):
    """action_statement : RETURN expression
                        | WRITE expression
                        | WHERE expression
                        | LOOP expression"""
    pass

def p_expression(p):
    """expression : operation_expression
                  | boolean_expression
                  | IDENTIFIER"""
    pass

def p_operation_expression(p):
    """operation_expression : expression PLUS expression
                            | expression MINUS expression
                            | expression STAR expression
                            | expression SLASH expression
                            | expression MOD expression
                            | expression NEQ expression
                            | expression LEQ expression
                            | expression GEQ expression
                            | expression LT expression
                            | expression GT expression
                            | LPAREN expression RPAREN
                            | NUMBER"""
    pass

def p_let_expression(p):
    """let_expression : LET IDENTIFIER
                      | LET MUT IDENTIFIER
                      | LET REF IDENTIFIER"""
    pass

def p_boolean_expression(p):
    """boolean_expression : TRUE
                          | FALSE"""
    pass

def p_function(p):
    """function : FN IDENTIFIER LPAREN list_parameters RPAREN LCURLY statements RCURLY
                | FN IDENTIFIER LPAREN list_parameters RPAREN type LCURLY statements RCURLY"""
    pass

def p_list_parameters(p):
    """list_parameters :
                       | IDENTIFIER type
                       | IDENTIFIER type COMMA list_parameters"""
    pass

def p_struct(p):
    """struct : STRUCT IDENTIFIER LCURLY statements RCURLY"""
    pass

def p_type(p):
    """type : INT
            | FLOAT
            | CHAR
            | STR
            | BOOLEAN"""
    pass

def p_error(p):
    if (p):
        print("Syntax error in input", p)

# Build Lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test program
textFile = open('Program_Test.txt', 'r')
data = textFile.read()
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
log = logging.getLogger()
parser.parse(data, lexer=lexer)