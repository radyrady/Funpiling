#-----------------------------------
# Jose Miguel Rady  920096
# Luis Ordaz        919790
#-----------------------------------
# Orientacion obtenida de la documentacion oficial de python
# http://www.dabeaz.com/ply/example.html

# Importa el modulo de PLY a ser utilizado para generar el analizador
# lexico
import ply.lex as lex

# --------------------Analizador Lexico-------------------------
# Lista de las palabras reservadas para el lenguaje
# Empleadas de esta forma como indicado por el tutorial para
# optimizar
reserved = {'main':'MAIN', 'if':'IF', 'else':'ELSE', 'print':'PRINT', 'bool': 'BOOL_ID','int':'INTEGER_ID', 'float':'FLOAT_ID', 'string':'STRING_ID','id':'ID','while':'WHILE','var':'VAR','void':'VOID', 'True': 'TRUE', 'False':'FALSE', 'return':'RETURN'}

# Lista de los nombres de los diferentes tokens (elementos terminales)
# Inclusion del grupo de palabras reservadas descrito previamente
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
   'COLON',
]+list(reserved.values())


# Expresiones regulares para los tokens simples
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
t_COLON = r'\:'

# Expresiones regulares para los tokens simples que incluyen
# acciones a ser realizadas
def t_ID(t):
    r'[A-z][A-z|0-9|\_A-z|\_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_FLOAT(t):
    r'[\-\+]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[\-\+]?[0-9]+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'\"(.)*\"'
    return t

def t_BOOL(t):
    r'(True|False)'
    t.value = bool(t.value)

# Define la regla para obtener el numero de linea para el manejo de errores
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres que son ignorados: espacios, tabs y comentarios
t_ignore  = ' \t'
t_ignore_COMMENT = r'//.*'

# Regla para el manejo de errores para identificar aquellos
# elementos que no pertenezcan al lexico
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Creacion del analizador lexico que provee el modulo PLY
lexer = lex.lex()

