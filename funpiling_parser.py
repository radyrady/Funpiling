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

# Declaracion de nuestras estructuras de datos 

directorio_variables_de_procs = {} # Diccionario
directorio_variables_referenciadas_a_memoria_raiz = {} # Diccionario
directorio_variables_referenciadas_a_memoria_temporal = {} # Diccionario
variables_actuales = [] # Lista
pila_operadores = []
pila_operandos = []
pila_saltos = []
nombreScope = ""
identificadorTemporal = 1
sonVariablesGlobales = 1
offsetOperaciones = 0
offsetGlobalesEnteras = 1
offsetGlobalesFloats = 50
offsetLocalesEnteras = 100
offsetLocalesFloats = 150

# --------------------Analizador Sintactico-------------------------
# Declaraciones de las diferentes reglas empleadas para generar las
# diferentes producciones del lenguaje. La primera produccion debe ser
# aquella considerada como la produccion inicial

def p_programa(p):
    '''programa : vars_globales seen_Vars_Globales funcion VOID MAIN seen_Main bloque seen_Programa 
    '''

# Regla que permite actualizar el directorio de variables locales del main en
# el diccionario raiz de procedimientos y agregarle una referencia a las variables globales
def p_seen_Programa(p):
    'seen_Programa : '
    global directorio_variables_de_procs
    global nombreScope
    global directorio_variables_referenciadas_a_memoria_raiz 
    global directorio_variables_referenciadas_a_memoria_temporal
    nombreScope = "main"
    directorio_variables_referenciadas_a_memoria_temporal["referencia_Globales"] = directorio_variables_referenciadas_a_memoria_raiz["globales"]
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_temporal = {}
    directorio_variables_de_procs = {}
    
def p_vars_globales(p):
    '''
      vars_globales : vars vars_globales
                | empty
    '''
# Regla que permite actualizar las variables actuales ya se en el contexto
# global, de una funcion o del main al actualizar la lista de variables actuales
def p_seen_Vars(p):
    'seen_Vars : '
    global variables_actuales
    variables_actuales.append(p[-1])

def p_seen_Main(p):
    'seen_Main : '
    global offsetLocalesEnteras
    global offsetLocalesFloats
    offsetLocalesEnteras = 100
    offsetLocalesFloats = 150
    directorio_variables_referenciadas_a_memoria_temporal = {} 
    
    
# Regla que permite actualizar el directorio de variables globales en el diccionario
# raiz de procedimientos
def p_seen_Vars_Globales(p):
    'seen_Vars_Globales : '
    global directorio_variables_de_procs
    global directorio_variables_referenciadas_a_memoria_temporal
    global sonVariablesGlobales
    global nombreScope
    nombreScope = "globales"
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_de_procs = {}
    directorio_variables_referenciadas_a_memoria_temporal = {}
    sonVariablesGlobales = 0
    

# Regla que identifica a todas las variables de un determinado tipo y actualiza
# el diccionario de las variables del procedimiento
def p_seen_Tipo(p):
    'seen_Tipo : '
    if p[-2] is ':':
        global directorio_variables_de_procs
        global variables_actuales
        global sonVariablesGlobales
        global offsetGlobalesEnteras 
        global offsetGlobalesFloats 
        global offsetLocalesEnteras 
        global offsetLocalesFloats
        global nombreScope
        global directorio_variables_referenciadas_a_memoria_raiz
        global directorio_variables_referenciadas_a_memoria_temporal
        if (p[-1] in directorio_variables_de_procs):
            directorio_variables_de_procs[p[-1]]['variables'].extend(variables_actuales)
        else:
            directorio_variables_de_procs[p[-1]] = {'variables':variables_actuales}
        variables_actuales = []

        if sonVariablesGlobales == 1:
            #print("---------------------> Son Globales")
            for a in directorio_variables_de_procs:
                if a == "int":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = offsetGlobalesEnteras
                            offsetGlobalesEnteras += 1
                elif a == "float":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = offsetGlobalesFloats
                            offsetGlobalesFloats += 1
                    
        else:
            #print("---------------------> Son Locales")
            for a in directorio_variables_de_procs:
                if a == "int":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = offsetLocalesEnteras
                            offsetLocalesEnteras += 1
                elif a == "float":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = offsetLocalesFloats
                            offsetLocalesFloats += 1
            

# Regla que permite actualizar el directorio de variables locales de cada funcion en
# el diccionario raiz de procedimientos y agregarle una referencia a las variables globales
def p_seen_Funcion(p):
    'seen_Funcion : '
    global directorio_raiz_procedimientos
    global directorio_variables_de_procs
    global directorio_variables_referenciadas_a_memoria_raiz 
    global directorio_variables_referenciadas_a_memoria_temporal
    global nombreScope
    nombreScope = p[-5]
    directorio_variables_referenciadas_a_memoria_temporal["referencia_Globales"] = directorio_variables_referenciadas_a_memoria_raiz["globales"]
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_de_procs = {}
    offsetLocalesEnteras = 100
    offsetLocalesFloats = 150
    directorio_variables_referenciadas_a_memoria_temporal = {}  

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
      asignacion : ID seen_Id EQUAL seen_Equals expresion DEL seen_Asignacion
    '''
def p_seen_Asignacion(p):
    'seen_Asignacion : '
    global pila_operadores
    global pila_operandos
    if pila_operadores:
            operador = pila_operadores.pop()
            operando = pila_operandos.pop()
            asignadoA = pila_operandos.pop()
            print('(', operador, operando, "null",asignadoA, ')')

def p_seen_Equals(p):
    'seen_Equals : '
    global pila_operadores
    pila_operadores.append(p[-1])
    

def p_seen_Id(p):
    'seen_Id : '
    global pila_operandos
    pila_operandos.append(p[-1])

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
      condicion : IF LPARENTH expresion RPARENTH bloque condicion_else
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
                | exp LTHAN seen_OperadorRelacional exp seen_Relacional
                | exp GTHAN seen_OperadorRelacional exp seen_Relacional
                | exp DIFF seen_OperadorRelacional exp seen_Relacional
                | exp SAME seen_OperadorRelacional exp seen_Relacional
    '''

def p_seen_OperadorRelacional(p):
    'seen_OperadorRelacional : '
    global pila_operadores
    pila_operadores.append(p[-1])

def p_seen_Relacional(p):
    'seen_Relacional : '
    'seen_Termino : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '==' or topePila == '<>' or topePila == '>' or topePila == '<':
            operador = pila_operadores.pop()
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            resultado = 't' + str(identificadorTemporal)
            identificadorTemporal += 1
            print('(', operador, operando1, operando2, resultado, ')')

def p_exp(p):
    '''
     exp : termino seen_Termino exp_aux
    '''

def p_seen_Termino(p):
    'seen_Termino : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '+' or topePila == '-':
            operador = pila_operadores.pop()
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            resultado = 't' + str(identificadorTemporal)
            identificadorTemporal += 1
            print('(', operador, operando1, operando2, resultado, ')')
            pila_operandos.append(resultado)
            
def p_exp_aux(p):
    '''
      exp_aux : PLUS seen_Plus exp
              | MINUS seen_Minus exp
              | empty
    '''

def p_seen_Plus(p):
    'seen_Plus : '
    global pila_operadores
    pila_operadores.append(p[-1])

def p_seen_Minus(p):
    'seen_Minus : '
    global pila_operadores
    pila_operadores.append(p[-1])

def p_termino(p):
    '''
      termino : factor seen_Factor termino_aux
    '''

def p_seen_Factor(p):
    'seen_Factor : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '*' or topePila == '/':
            operador = pila_operadores.pop()
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            resultado = 't' + str(identificadorTemporal)
            identificadorTemporal += 1
            print('(', operador, operando1, operando2, resultado, ')')
            pila_operandos.append(resultado)

def p_termino_aux(p):
    '''
      termino_aux : TIMES seen_Times termino
                  | DIVIDE seen_Divide termino
                  | empty
    '''

def p_seen_Times(p):
    'seen_Times : '
    global pila_operadores
    pila_operadores.append(p[-1])

def p_seen_Divide(p):
    'seen_Divide : '
    global pila_operadores
    pila_operadores.append(p[-1])

def p_factor(p):
    '''
      factor : ID seen_Id 
             | factor_sign INTEGER seen_Id
             | factor_sign FLOAT seen_Id
             | LPARENTH seen_Leftparenth exp RPARENTH seen_Rightparenth
             | STRING 
             | ID LPARENTH expresion escritura_expresion_aux RPARENTH 
    '''

def p_seen_Leftparenth(p):
    'seen_Leftparenth : '
    global pila_operadores
    pila_operadores.append("(")
    

def p_seen_Rightparenth(p):
    'seen_Rightparenth : '
    global pila_operadores
    pila_operadores.reverse()
    pila_operadores.remove("(")
    pila_operadores.reverse()
    
    
def p_factor_sign(p):
    '''
      factor_sign : PLUS 
                  | MINUS 
                  | empty
    '''

# Regla sintactica que identifica un error de sintaxis
def p_error(p):
    print("Syntax error in input!", p)

# Creacion del parser en relacion a las reglas sintacticas generadas
# y a los tokens creados por medio del analizador lexico
parser = yacc.yacc(debug=True)


# Seccion de pruebas obteniendo como entrada un archivo de texto
f = open("Prueba2.txt")
datos = f.read()
print(datos)

print()
print("----------------------------------------------------")
print("||                Cuadruplos                     ||")
print("----------------------------------------------------")
print()
# Aplicacion del analizador lexico y sintactico a la entrada
logging.basicConfig(filename='example.log',level=logging.INFO)
log = logging.getLogger('example.log')
result = parser.parse(datos,debug=log)

## Seccion de pruebas para mostrar como se da la exploracion de nuestras
## tablas de simbolos
print()
print("----------------------------------------------------")
print("||    Contenidos de nuestras tablas de simbolos   ||")
print("----------------------------------------------------")
print()

for a in directorio_variables_referenciadas_a_memoria_raiz:
    print("----------------")
    if a == "globales":
        print("Nivel A------> ", a)
        for b in directorio_variables_referenciadas_a_memoria_raiz[a]:
            print("\tNivel B------> ", b ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b])
    else:
        print("Nivel A------> ", a)
        for b in directorio_variables_referenciadas_a_memoria_raiz[a]:
            if b != "referencia_Globales":
                print ("\t\tNivel B------> ", b ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b])
            else:
                print ("\t\tNivel B------> ", b) 
                for c in directorio_variables_referenciadas_a_memoria_raiz[a][b]:
                    print ("\t\t\tNivel C------> ", c ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c])

## ---------------------------------------------------------------------------------------------
## Ejemplos de busquedas
## print(directorio_variables_referenciadas_a_memoria_raiz["globales"]["dos"])
## print(directorio_variables_referenciadas_a_memoria_raiz["func"]["referencia_Globales"]["dos"])
## ---------------------------------------------------------------------------------------------
##


                    
