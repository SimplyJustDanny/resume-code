import logging
import ply.lex as lex
import ply.yacc as yacc

# Keywords for easy conversion of regex to tokens
keywords = {
    'if' : 'IF', 'else' : 'ELSE', 'while' : 'WHILE', 'let' : 'LET',
    'loop' : 'LOOP', 'fn' : 'FN', 'mut' : 'MUT', 'ref' : 'REF',
    'struct' : 'STRUCT', 'return' : 'RETURN', 'true' : 'TRUE',
    'false' : 'FALSE', 'where' : 'WHERE', 'write' : 'WRITE', 'int' : 'INT',
    'i8' : 'INT', 'i16' : 'INT', 'i32' : 'INT', 'i64' : 'INT', 'u8' : 'INT',
    'u16' : 'INT', 'u32' : 'INT', 'u64' : 'INT', 'float' : 'FLOAT',
    'f32' : 'FLOAT', 'f32' : 'FLOAT', 'çhar' : 'CHAR', 'str': 'STR',
    'String': 'STR', 'boolean' : 'BOOLEAN', 'bool' : 'BOOLEAN',
}

tokens = [
    'IDENTIFIER', 'NUMBER',
    # Delimiters
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'COLON', 'SEMICOLON',  'COMMA',  'POINT', 'APOS', 'RARROW',
    # Operators
    'EQUALS', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT', 'PLUS', 'MINUS', 'MULT', 'DIV', 
    'MOD', 'ASSIGN',
] + list(set(keywords.values()))

# Make sure operations retain a specific order to remove ambiguity
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'EQUALS', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT'),
)

# Dictionaries and lists for things like vars, functions and returns
variables = {}
functions = {"println":{"parameters": ["string"], "body": [""]}, "println!":{"parameters": ["string"], "body": [""]}}
funcreturns = []
whiles = {}
structs = {}
returns = []

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

# Token matching rules are written as regexs
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_COLON     = r':'
t_SEMICOLON = r';'
t_COMMA     = r','
t_RARROW    = r'->'

t_EQUALS    = r'=='
t_NEQ       = r'!='
t_LEQ       = r'<='
t_GEQ       = r'>='
t_LT        = r'<'
t_GT        = r'>'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULT      = r'\*'
t_DIV       = r'/'
t_MOD       = r'%'
t_ASSIGN    = r'='
t_POINT     = r'.' 
t_APOS      = r'\''

# Regular expression for identifiers, which parses keywords in the token list
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, "IDENTIFIER")
    return t

# Regular expression for numbers, which are then parsed as ints
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# A few helper functions regarding types and parameters
def default(p):
    if p in ["i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64", "int"]:
        return 0
    if p in ["bool", "boolean"]:
        return False
    if p in ["char", "String", "str"]:
        return ""
    if p in ["f32", "f64", "float"]:
        return 0.0
    
def gettype(expression):
    if (isinstance(expression, int) and type(expression) == int) or expression  in ["i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64", "int"]:
        return "int"
    if (isinstance(expression, float) and type(expression) == float) or expression in ["f32", "f64", "float"]:
        return "float"
    if (isinstance(expression, bool) and type(expression) == bool) or expression == ["bool", "boolean"]:
        return "bool"
    if (isinstance(expression, str) and type(expression) == str) or expression == ["String", "str"]:
        return "String"
    return "char"

def is_valid_params(name, args):
    if functions[name]["parameters"] == None:
        return args == [None]
    if len(functions[name]["parameters"]) != len(args):
        print(f"function parameters don't match ones found in definition")
        return False
    return True

# Define the parser functions
def p_program(p):
    """program : statements"""
    p[0] = p[1]

def p_statements(p):
    """statements : statement
                  | statements statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    """statement : assignment_statement
                 | if_statement
                 | if_else_statement
                 | while_statement
                 | action_statement
                 | let_expression                 
                 | function
                 | struct"""
    p[0] = p[1]

def p_assignment_statement(p):
    """assignment_statement : let_expression ASSIGN expression SEMICOLON
                            | let_expression SEMICOLON
                            | IDENTIFIER ASSIGN expression SEMICOLON"""
    if len(p) == 5:
        variables[p[1]] = p[3]
    else:
        variables[p[1]] = None
    
def p_if_statement(p):
    """if_statement : IF expression LCURLY statements RCURLY"""
    if p[2]:
        p[0] = p[4]
    else:
        p[0] = None
        
def p_if_else_statement(p):
    """if_else_statement : IF expression LCURLY statements RCURLY ELSE LCURLY statements RCURLY
                         | IF expression LCURLY statements RCURLY ELSE if_statement
                         | IF expression LCURLY statements RCURLY ELSE if_statement ELSE LCURLY statements RCURLY"""
    if len(p) == 10:
        if p[2]:
            p[0] = p[4]
        else:
            p[0] = p[8]
    elif len(p) == 8:
        if p[2]:
            p[0] = p[4]
        else:
            p[0] = p[7]
    elif len(p) == 12:
        if p[2]:
            p[0] = p[4] 
        elif p[7]:
            p[0] = p[7] 
        else:
            p[0] = p[10]

def p_while_statement(p):
    """while_statement : WHILE expression LCURLY statements RCURLY"""
    if (p[2] not in variables) and (str(p[2]) != "True") and (str(p[2]) != "False"):
        print(f"(Line '{p.lineno(2)}') Variable Error: Variable '{p[2]}' used in while loop not defined.")
        p[0] = None
    else:
        whiles[p[2]] = {"expression" : p[2], "statements" : p[4]}
        p[0] = {"expression" : p[2], "statements" : p[4]}

def p_action_statement(p):
    """action_statement : RETURN expression SEMICOLON
                        | WRITE expression SEMICOLON
                        | WHERE expression SEMICOLON
                        | LOOP expression SEMICOLON"""
    if p[1] == 'return':
        if p[2] in variables:
            returns.append(gettype(variables[p[2]]))
        else:
            returns.append(gettype(p[2]))
    p[0] = p[2]
    
def p_expression(p):
    """expression : operation_expression
                  | boolean_expression
                  | char_expression
                  | type_expression
                  | IDENTIFIER"""     
    p[0] = p[1]

def p_operation_expression(p):
    """operation_expression : expression PLUS expression
                            | expression MINUS expression
                            | expression MULT expression
                            | expression DIV expression
                            | expression MOD expression
                            | expression EQUALS expression
                            | expression NEQ expression
                            | expression LEQ expression
                            | expression GEQ expression
                            | expression LT expression
                            | expression GT expression
                            | LPAREN expression RPAREN
                            | NUMBER"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[1] = variables.get(p[1], p[1])
        p[3] = variables.get(p[3], p[3])
        if type(p[1]) != type(p[3]):
            print(f"(Line '{p.lineno(2)}') Type Error: Type mismatch in operation '{p[2]}' between {type(p[1]).__name__} and {type(p[3]).__name__}.")
            p[0] = None
        elif p[2] in ["+", "-", "*", "/", "%"]:
            if (type(p[1]) == str) or (type(p[1]) == bool):
                    print(f"(Line '{p.lineno(2)}') Type Error: Unsupported operand type for '{p[2]}': {type(p[1]).__name__}.")
                    p[0] = None
            elif p[2] == "+":
                p[0] = p[1] + p[3]
            elif p[2] == "-":
                p[0] = p[1] - p[3]
            elif p[2] == "*":
                p[0] = p[1] * p[3]
            elif p[2] == "/":
                if p[3] == 0:
                    print(f"(Line '{p.lineno(2)}') Division Error: Cannot perform division by zero.")
                    p[0] = None
                else:
                    p[0] = p[1] / p[3]
            elif p[2] == "%":
                if p[3] == 0:
                    print(f"(Line '{p.lineno(2)}') Modulo Error: Cannot perform modulo by zero.")
                    p[0] = None
                else:
                    p[0] = p[1] % p[3]
        elif p[2] == "==":
            p[0] = p[1] == p[3]
        elif p[2] == "!=":
            p[0] = p[1] != p[3]
        elif p[2] == "<=":
            p[0] = p[1] <= p[3]
        elif p[2] == ">=":
            p[0] = p[1] >= p[3]
        elif p[2] == "<":
            p[0] = p[1] < p[3]
        elif p[2] == ">":
            p[0] = p[1] > p[3]
        else:
            p[0] = p[2]
 
def p_type_expression(p):
    """type_expression : IDENTIFIER COLON BOOLEAN
                       | IDENTIFIER COLON CHAR
                       | IDENTIFIER COLON INT
                       | IDENTIFIER COLON FLOAT
                       | IDENTIFIER COLON STR"""
    variables[p[1]] = {"explicit" : True, "type" : p[3], "content" : ""}
    p[0] = p[1]

def p_let_expression(p):
    """let_expression : LET IDENTIFIER
                      | LET MUT IDENTIFIER
                      | LET REF IDENTIFIER
                      | LET type_expression
                      | LET MUT type_expression
                      | LET REF type_expression"""
    if len(p) == 3:
        if p[2] not in variables:
            variables[p[2]] = {"explicit" : False, "type" : "", "content" : ""}
        p[0] = p[2]
    elif len(p) == 4:
        if p[3] not in variables:
            variables[p[3]] = {"explicit" : False, "type" : "", "content" : ""}
        p[0] = p[3]

def p_char_expression(p):
    """char_expression : APOS IDENTIFIER APOS
                       | APOS APOS
                       | APOS NUMBER APOS"""
    if len(p) == 4:
        if gettype(p[2]) == 'int' and 0 <= p[2] <= 9:
            p[0] = f'{p[2]}'
        elif gettype(p[2]) != 'int' and len(p[2]) == 1:
            p[0] = f'{p[2]}'
        else:
            print(f"(Line '{p.lineno(2)}') Type Error: Char can only be one character.")
    elif len(p) == 3:
        p[0] = p[0]

def p_boolean_expression(p):
    """boolean_expression : TRUE
                          | FALSE"""
    p[0] = p[1] == 'true'
    
def p_argument(p):
    """argument :
                | IDENTIFIER
                | expression"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 1:
        p[0] = None

def p_arguments(p):
    """arguments : argument
                 | argument COMMA arguments"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_function(p):
    """function : FN IDENTIFIER LPAREN list_parameters RPAREN RARROW type LCURLY statements RCURLY
                | IDENTIFIER LPAREN arguments RPAREN SEMICOLON"""
    if len(p) == 6:
        if p[1] in functions:
            if not is_valid_params(p[1], p[3]):
                print(f"(Line '{p.lineno(2)}') Parameter Error: Function parameters don't match.")
                p[0] = None
            else:
                p[0] = functions[p[1]]
        else:
            print(f"(Line '{p.lineno(2)}') Function Error: Function '{p[1]}' is undefined.")
            return
    elif len(p) == 11:
        functions[p[2]] = {"parameters" : p[4], "return_type" : p[7], "body" : p[9]}
        funcreturns.append(p[7])
        p[0] = functions[p[2]]
        if len(returns) == 0 or len(funcreturns) != len(returns):
            print(f"(Line '{p.lineno(2)}') Return Error: Function '{p[2]}' does not return or returns more than once.")
            p[0] = None
            return
        if funcreturns[-1] != returns[-1]:
            print(f"(Line '{p.lineno(2)}') Return Error: Function '{p[2]}' return differs from what was defined.")
            p[0] = None
            return

def p_list_parameters(p):
    """list_parameters :
                       | IDENTIFIER COLON type
                       | IDENTIFIER COLON type COMMA
                       | IDENTIFIER COLON type COMMA list_parameters"""
    if len(p) == 4 or len(p) == 5:
        variables[p[1]] = default(p[3])
        p[0] = [p[1]]
    elif len(p) == 6:
        variables[p[1]] = default(p[3])
        p[0] = [p[1]] + p[5]

def p_struct(p):
    """struct : STRUCT IDENTIFIER LCURLY list_parameters RCURLY
              | IDENTIFIER POINT expression SEMICOLON"""
    if len(p) == 6:
        structs[p[2]] = {"name" : p[2], "fields" : p[4]}
        p[0] = {"name" : p[2], "fields" : p[4]}
    else:
        if p[1] in structs and p[3] in variables:
            p[0] = variables[p[3]]
        else:
            print(f"(Line '{p.lineno(2)}') Struct Error: Struct '{p[1]}' and/or field '{p[1]}' are undeclared.")
            p[0] = None

def p_type(p):
    """type : INT
            | FLOAT
            | CHAR
            | STR
            | BOOLEAN"""
    p[0] = p[1]

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
parser.parse(data, debug=log)