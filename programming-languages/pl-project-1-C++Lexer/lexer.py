import ply.lex as lex

tokens = [
    'IDENTIFIER', 'NUMBER',
    # Keywords
    'IF', 'ELSE', 'WHILE', 'LET', 'LOOP', 'FN', 'MUT', 'PUB', 'REF', 'IN',
    'STRUCT', 'TYPE', 'RETURN', 'TRUE', 'FALSE', 'WHERE', 'WRITE',
    # Delimiters
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY','LSQR', 'RSQR', 'SEMICOLON', 'COMMA',
    # Operators
    'EQUALS', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT', 'PLUS', 'MINUS', 'STAR', 'SLASH', 'MOD'
]

# Handlers that ignore whitespace, comments, newlines, and print illegal chars respectively
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
t_IF        = 'if'
t_ELSE      = 'else'
t_WHILE     = 'while'
t_LET       = 'let'
t_LOOP      = 'loop'
t_FN        = 'fn'
t_MUT       = 'mut'
t_PUB       = 'pub'
t_REF       = 'ref'
t_IN        = 'in'
t_STRUCT    = 'struct'
t_TYPE      = 'type'
t_RETURN    = 'return'
t_TRUE      = 'true'
t_FALSE     = 'false'
t_WHERE     = 'where'
t_WRITE     = 'write'

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
    check = t.value.upper()
    if check in tokens: t.type = check
    return t

# Regular expression for numbers, which are then parsed as ints
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Build Lexer
lexer = lex.lex()

# Test program
textFile = open('Program_Test.txt', 'r')
data = textFile.read()
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)