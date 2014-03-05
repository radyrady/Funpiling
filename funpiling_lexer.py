import ply.lex as lex

reserved = {'main':'MAIN', 'if':'IF', 'else':'ELSE', 'print':'PRINT','int':'INTEGER_ID', 'float':'FLOAT_ID', 'string':'STRING_ID','id':'ID','while':'WHILE'}

# List of token names.   This is always required
tokens = [
   'PLUS',
   'MINUS',
   'INTEGER',
   'FLOAT',
   'STRING',
   'TIMES',
   'DIVIDE',
   'LPARENTH',
   'RPARENTH',
   'LTHAN',
   'GTHAN',
   'DIFF',
   'DEL',
   'COMMA',
   'LBRACE',
   'RBRACE',
   'EQUAL',
   'SAME',
]+list(reserved.values())


# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPARENTH  = r'\('
t_RPARENTH  = r'\)'
t_LTHAN = r'\<'
t_GTHAN = r'\>'
t_DIFF = r'\<\>'
t_DEL = r'\;'
t_COMMA = r'\,'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQUAL = r'\='
t_SAME = r'\=='


def t_ID(t):
    r'[A-z][A-z|0-9|\_A-z|\_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_FLOAT(t):
    r'[\-\+]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# A regular expression rule with some action code
def t_INTEGER(t):
    r'[\-\+]?[0-9]+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'([\"][A-z]+[\"])|([\'][A-z]+[\'])'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
    int d;

    int luis(int lol, float damn){
       k = 6;
    }
    
    int main{
         l_0_9 = 5;
    }
'''

# Give the lexer some input
lexer.input(data)
# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print(tok)

