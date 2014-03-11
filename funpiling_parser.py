#-----------------------------------
# Jose Miguel Rady  920096
# Luis Ordaz        919790
#-----------------------------------
# Orientacion obtenida de la documentacion oficial de python
# http://www.dabeaz.com/ply/example.html

# Importa el modulo de PLY a ser utilizado para generar el analizador
# sintactico (parser)
import logging
import ply.yacc as yacc

# Importa los tokens generados por el analizador lexico (Esto es requerido)
from funpiling_lexer import tokens

# Declaracion de nuestra estructura de datos Dictionary
directorio_raiz_procedimientos = {}
directorio_variables_de_procs = {}
variables_actuales = []

# --------------------Analizador Sintactico-------------------------
# Declaraciones de las diferentes reglas empleadas para generar las
# diferentes producciones del lenguaje. La primera produccion debe ser
# aquella considerada como la produccion inicial



def p_programa(p):
    '''programa : vars_main seen_Vars_Main funcion VOID MAIN bloque seen_Programa 
    '''

def p_seen_Programa(p):
    'seen_Programa : '
    #print(p[-1])
    global directorio_raiz_procedimientos
    global directorio_variables_de_procs
    directorio_raiz_procedimientos['main'] = {'locales': directorio_variables_de_procs}
    directorio_raiz_procedimientos['main']['globales'] = directorio_raiz_procedimientos['globals'] 
    directorio_variables_de_procs = {}
    
def p_vars_main(p):
    '''
      vars_main : vars vars_main
                | empty
    '''

def p_seen_Vars(p):
    'seen_Vars : '
    global variables_actuales
    #print(p[-1])
    variables_actuales.append(p[-1])
    

def p_seen_Vars_Main(p):
    'seen_Vars_Main : '
    #print("ENTRO AQUI VARS MAIN")
    global directorio_raiz_procedimientos
    global directorio_variables_de_procs
    directorio_raiz_procedimientos['globals'] = directorio_variables_de_procs
    directorio_variables_de_procs = {}

def p_seen_Tipo(p):
    'seen_Tipo : '
    if p[-2] is ':':
        global directorio_variables_de_procs
        global variables_actuales
        #print(p[-1])
        directorio_variables_de_procs[p[-1]] = {'variables':variables_actuales}
        #print(directorio_variables_de_procs)
        variables_actuales = []

def p_seen_Funcion(p):
    'seen_Funcion : '
    #print(directorio_variables_de_procs)
    #print(p[-5])
    global directorio_raiz_procedimientos
    global directorio_variables_de_procs
    directorio_raiz_procedimientos[p[-5]] = {'locales': directorio_variables_de_procs}
    directorio_raiz_procedimientos[p[-5]]['globales'] = directorio_raiz_procedimientos['globals'] 
    directorio_variables_de_procs = {}
    #print("ENTRO AQUI FUNCION")

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
      funcion : tipo ID LPARENTH vars_funcion RPARENTH bloque seen_Funcion funcion
              | empty
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
      vars : VAR ID seen_Vars vars_aux COLON tipo DEL
      
    '''

def p_vars_aux(p):
    '''
      vars_aux : COMMA ID seen_Vars vars_aux
               | empty
    '''

def p_tipo(p):
    '''
      tipo : INTEGER_ID seen_Tipo
           | FLOAT_ID seen_Tipo
           | STRING_ID seen_Tipo
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

# Regla sintactica que identifica un error de sintaxis
def p_error(p):
    print("Syntax error in input!")

# Creacion del parser en relacion a las reglas sintacticas generadas
# y a los tokens creados por medio del analizador lexico
parser = yacc.yacc(debug=True)


# Seccion de pruebas obteniendo como entrada un archivo de texto
f = open("Prueba.txt")
datos = f.read()
print(datos)

# Aplicacion del analizador lexico y sintactico a la entrada
logging.basicConfig(filename='example.log',level=logging.INFO)
log = logging.getLogger('example.log')
result = parser.parse(datos,debug=log)
print(directorio_raiz_procedimientos)
