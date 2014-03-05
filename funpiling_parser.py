# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from funpiling_lexer import tokens

# Declaring our dataStruct Dictionary
proc_name_list = []
proc_dictionary = {}
proc_vars = {}
proc_vars_type = []
proc_vars_final = {}
proc_datos={}

def p_programa(p):
    '''programa : tipo MAIN seen_Programa bloque
                | programa_vars seen_Vars programa_funcion seen_Funcion tipo MAIN seen_Programa bloque
    '''

def p_seen_Programa(p):
    'seen_Programa : '
    print("ENTRO AQUI MAIN SOLO")

    
def p_programa_vars(p):
    '''
      programa_vars : vars
    '''
def p_seen_Vars(p):
    'seen_Vars : '
    print("ENTRO AQUI VARS")


def p_programa_funcion(p):
    '''
      programa_funcion : funcion
    '''

def p_seen_Funcion(p):
    'seen_Funcion : '
    print("ENTRO AQUI FUNCION")


def p_empty(p):
    'empty : '
    pass

def p_bloque(p):
    '''
      bloque : LBRACE bloque_estatuto RBRACE
    '''

def p_bloque_estatuto(p):
    '''
       bloque_estatuto : estatuto bloque_estatuto
                       | empty
    '''

def p_estatuto(p):
    '''
      estatuto : asignacion
               | llamada_funcion
               | condicion
               | escritura
               | vars
               | while_loop
    '''

def p_funcion(p):
    '''
      funcion : tipo ID LPARENTH vars_funcion RPARENTH bloque
    '''

def p_vars_funcion(p):
    '''
      vars_funcion : tipo ID vars_funcion_aux
                   | empty
    '''

def p_vars_funcion_aux(p):
    '''
      vars_funcion_aux : COMMA tipo ID vars_funcion_aux
                       | empty
    '''

def p_while_loop(p):
    '''
      while_loop : WHILE LPARENTH expresion RPARENTH bloque
    '''

def p_asignacion(p):
    '''
      asignacion : ID EQUAL expresion DEL
    '''

def p_llamada_funcion(p):
    '''
      llamada_funcion : ID LPARENTH llamada_funcion_expresion RPARENTH DEL
    '''

def p_llamada_funcion_expresion(p):
    '''
      llamada_funcion_expresion : expresion llamada_funcion_expresion_aux
                                | empty
    '''

def p_llamada_funcion_expresion_aux(p):
    '''
      llamada_funcion_expresion_aux : COMMA expresion llamada_funcion_expresion_aux
                                    | empty
    '''

def p_condicion(p):
    '''
      condicion : IF LPARENTH expresion bloque condicion_else
    '''

def p_condicion_else(p):
    '''
      condicion_else : ELSE bloque
                     | empty
    '''

def p_escritura(p):
    '''
      escritura : PRINT LPARENTH expresion escritura_expresion_aux RPARENTH DEL
    '''

def p_escritura_expresion_aux(p):
    '''
      escritura_expresion_aux : COMMA expresion escritura_expresion_aux
                              | empty
    '''

def p_vars(p):
    '''
      vars : tipo ID vars_aux DEL
    '''

def p_vars_aux(p):
    '''
      vars_aux : COMMA ID vars_aux
               | empty
    '''

def p_tipo(p):
    '''
      tipo : INTEGER_ID
           | FLOAT_ID
           | STRING_ID
    '''

def p_expresion(p):
    '''
      expresion : exp
                | LTHAN exp
                | GTHAN exp
                | DIFF exp
                | SAME exp
    '''

def p_exp(p):
    '''
      exp : termino exp_aux
    '''

def p_exp_aux(p):
    '''
      exp_aux : PLUS exp
              | MINUS exp
              | empty
    '''

def p_termino(p):
    '''
      termino : factor termino_aux
    '''

def p_termino_aux(p):
    '''
      termino_aux : TIMES termino
                  | DIVIDE termino
                  | empty
    '''

def p_factor(p):
    '''
      factor : ID
             | factor_sign INTEGER
             | factor_sign FLOAT
             | LPARENTH exp RPARENTH
             | STRING
             | ID LPARENTH expresion escritura_expresion_aux RPARENTH
    '''

def p_factor_sign(p):
    '''
      factor_sign : PLUS
                  | MINUS
                  | empty
    '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

s = '''
    int d;

    int luis(int lol, float damn){
       k = 6;
    }
    
    int main{
         l_0_9 = 5;
    }
'''

result = parser.parse(s)

