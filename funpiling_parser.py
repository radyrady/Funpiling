#-----------------------------------
# Jose Miguel Rady  920096
# Luis Ordaz        919790
#-----------------------------------
# Orientacion obtenida de la documentacion oficial de python
# http://www.dabeaz.com/ply/example.html

# Importa el modulo de PLY a ser utilizado para generar el analizador
# sintactico (parser)
from Classes import *
import logging
import ply.yacc as yacc


# Importa los tokens generados por el analizador lexico (Esto es requerido)
from funpiling_lexer import tokens

# Declaracion de nuestras estructuras de datos 

cubo_combinaciones = {'int':{
    'int':{'+':'int','-':'int','*':'int','/':'int','<':'bool','>':'bool','<>':'bool','&&':'error','||':'error','!=':'bool','==':'bool','=':'yes'},
    'float':{'+':'float','-':'float','*':'float','/':'float','<':'bool','>':'bool','<>':'bool','&&':'error','||':'error','!=':'bool','==':'bool','=':'error'},
    'string':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
    'bool':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'}
        },
    'float':{
        'int':{'+':'float','-':'float','*':'float','/':'float','<':'bool','>':'bool','<>':'bool','&&':'error','||':'error','!=':'bool','==':'bool','=':'yes'},
        'float':{'+':'float','-':'float','*':'float','/':'float','<':'bool','>':'bool','<>':'bool','&&':'error','||':'error','!=':'bool','==':'bool','=':'yes'},
        'string':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
        'bool':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'}
        },
    'string':{
        'int':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
        'float':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
        'string':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'bool','&&':'error','||':'error','!=':'bool','==':'bool','=':'yes'},
        'bool':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'}
        },
    'bool':{
        'int':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
        'float':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
        'string':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'error','&&':'error','||':'error','!=':'error','==':'error','=':'error'},
        'bool':{'+':'error','-':'error','*':'error','/':'error','<':'error','>':'error','<>':'bool','&&':'error','||':'error','!=':'bool','==':'bool','=':'yes'}
    }
}
directorio_raiz_procedimientos = {} #Diccionario
directorio_constantes = {}
directorio_temporales = {}
directorio_variables_de_procs = {} # Diccionario
directorio_variables_referenciadas_a_memoria_raiz = {} # Diccionario
directorio_variables_referenciadas_a_memoria_temporal = {} # Diccionario
parametros_referenciados_a_memoria_temporal = ""
variables_actuales = [] # Lista
tipo_funcion = [] # Lista
funcion_actual_trabajando = [] #Lista
cuadruplos = []
cuadruplo_temporal = Cuadruplo()
pila_operadores = []
pila_operandos = []
pila_saltos = []
pila_salto_main = []
nombreScope = ""
tipoParametro = ""
identificadorTemporal = 1
sonVariablesGlobales = 1
offsetOperaciones = 0
offsetGlobalesEnteras = 1
offsetGlobalesFloats = 50
offsetLocalesEnteras = 100
offsetLocalesFloats = 150
offsetConstantesEnteras = 200
offsetConstantesFlotantes = 250
cont = 0
contador_de_parametros = 0
contador_de_ints_locales = 0
contador_de_floats_locales = 0
contador_de_ints_globales = 0
contador_de_floats_globales = 0

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
    global contador_de_ints_locales
    global contador_de_floats_locales
    global contador_de_ints_globales
    global contador_de_floats_globales
    nombreScope = "main"
    directorio_variables_referenciadas_a_memoria_temporal["referencia_Globales"] = directorio_variables_referenciadas_a_memoria_raiz["globales"]
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["variables"] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_temporal = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["size"] = {'int':contador_de_ints_locales, 'float':contador_de_floats_locales}
    parametros_referenciados_a_memoria_temporal = ""
    directorio_variables_de_procs = {}
    contador_de_ints_locales = 0
    contador_de_floats_locales = 0
    
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
    global parametros_referenciados_a_memoria_temporal
    global cont
    global cuadruplos
    offsetLocalesEnteras = 100
    offsetLocalesFloats = 150
    directorio_variables_referenciadas_a_memoria_temporal = {}
    parametros_referenciados_a_memoria_temporal = ""
    #print(cont)
    #cont += 1
    inicio = pila_saltos.pop()
    cuadruplos[inicio].set_resultado(cont)
    
    
    
# Regla que permite actualizar el directorio de variables globales en el diccionario
# raiz de procedimientos
def p_seen_Vars_Globales(p):
    'seen_Vars_Globales : '
    global directorio_variables_de_procs
    global directorio_variables_referenciadas_a_memoria_temporal
    global sonVariablesGlobales
    global nombreScope
    global cuadruplos
    global cuadruplo_temporal
    global cont
    nombreScope = "globales"
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["variables"] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["size"] = {'int':contador_de_ints_globales, 'float':contador_de_floats_globales}
    directorio_variables_de_procs = {}
    directorio_variables_referenciadas_a_memoria_temporal = {}
    sonVariablesGlobales = 0
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("goto")
    cuadruplos.append(cuadruplo_temporal)
    print(cont)
    cont += 1
    pila_saltos.append(cont-1)
    

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
        global contador_de_ints_locales
        global contador_de_floats_locales
        global contador_de_ints_globales 
        global contador_de_floats_globales

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
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesEnteras, 'tipo':a}
                            offsetGlobalesEnteras += 1
                            contador_de_ints_globales+= 1
                elif a == "float":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesFloats, 'tipo':a}
                            offsetGlobalesFloats += 1
                            contador_de_floats_globales += 1
                    
        else:
            #print("---------------------> Son Locales")
            for a in directorio_variables_de_procs:
                if a == "int":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesEnteras, 'tipo':a}
                            offsetLocalesEnteras += 1
                            contador_de_ints_locales +=1
                elif a == "float":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesFloats, 'tipo':a}
                            offsetLocalesFloats += 1
                            contador_de_floats_locales += 1

    elif p[-2] == '(' or p[-2] == ',':
        global tipoParametro
        tipoParametro = p[-1]

    else:
        #print("AQUI ENTRO",p[-1])
        global tipo_funcion
        tipo_funcion.append(p[-1])
            
# Regla que permite actualizar el directorio de variables locales de cada funcion en
# el diccionario raiz de procedimientos y agregarle una referencia a las variables globales
def p_seen_Funcion(p):
    'seen_Funcion : '
    global directorio_raiz_procedimientos
    global directorio_variables_de_procs
    global directorio_variables_referenciadas_a_memoria_raiz 
    global directorio_variables_referenciadas_a_memoria_temporal
    global parametros_referenciados_a_memoria_temporal
    global contador_de_parametros
    global tipo_funcion
    global nombreScope
    global offsetLocalesEnteras
    global offsetLocalesFloats
    global contador_de_ints_locales
    global contador_de_floats_locales
    global contador_de_ints_globales
    global contador_de_floats_globales
    global cont
    global cuadruplos
    global cuadruplo_temporal
    nombreScope = p[-5]
    directorio_variables_referenciadas_a_memoria_temporal["referencia_Globales"] = directorio_variables_referenciadas_a_memoria_raiz["globales"]
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["variables"] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["parametros"] = parametros_referenciados_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["size"] = {'int':contador_de_ints_locales, 'float':contador_de_floats_locales}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["tipo"] = tipo_funcion.pop()
    directorio_variables_de_procs = {}
    offsetLocalesEnteras = 100
    offsetLocalesFloats = 150
    directorio_variables_referenciadas_a_memoria_temporal = {}
    parametros_referenciados_a_memoria_temporal = ""
    contador_de_parametros = 0
    contador_de_ints_locales = 0
    contador_de_floats_locales = 0
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("retorno")
    cuadruplos.append(cuadruplo_temporal)
    print(cont)
    cont += 1


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
      vars_funcion : tipo ID seen_Param vars_funcion_aux
                   | empty
    '''

def p_vars_funcion_aux(p):
    '''
      vars_funcion_aux : COMMA tipo ID seen_Param vars_funcion_aux
                       | empty
    '''

def p_seen_Param(p):
    'seen_Param : '
    global contador_de_ints_locales
    global contador_de_floats_locales
    global contador_de_parametros
    global tipoParametro
    global directorio_variables_referenciadas_a_memoria_temporal
    global parametros_referenciados_a_memoria_temporal
    global offsetLocalesFloats
    global offsetLocalesEnteras
    idParametro = p[-1]
    if tipoParametro == "int":
        if idParametro not in directorio_variables_referenciadas_a_memoria_temporal:
            directorio_variables_referenciadas_a_memoria_temporal[idParametro] = {'tipo':tipoParametro, 'dir_virtual':offsetLocalesEnteras}
            offsetLocalesEnteras += 1
            contador_de_ints_locales += 1
            if parametros_referenciados_a_memoria_temporal == "":
                parametros_referenciados_a_memoria_temporal = tipoParametro
            else:
                parametros_referenciados_a_memoria_temporal += ", " + tipoParametro
    elif tipoParametro == "float":
        if idParametro not in directorio_variables_referenciadas_a_memoria_temporal:
            directorio_variables_referenciadas_a_memoria_temporal[idParametro] = {'tipo':tipoParametro, 'dir_virtual': offsetLocalesFloats}
            offsetLocalesFloats += 1
            contador_de_floats_locales += 1
            if parametros_referenciados_a_memoria_temporal == "":
                parametros_referenciados_a_memoria_temporal = tipoParametro
            else:
                parametros_referenciados_a_memoria_temporal += ", " + tipoParametro
    contador_de_parametros = contador_de_parametros + 1


    
def p_while_loop(p):
    '''
      while_loop : WHILE seen_While LPARENTH expresion RPARENTH seen_Do bloque seen_Cycle
    '''

def p_seen_While(p):
    'seen_While : '
    global pila_saltos
    pila_saltos.append(cont)

def p_seen_Do(p):
    'seen_Do : '
    global pila_operandos
    global cuadruplo_temporal
    global cuadruplos
    global cont
    global pila_saltos
    if(True):
        cuadruplo_temporal = Cuadruplo()
        resultado = pila_operandos.pop()
        cuadruplo_temporal.set_operador("GotoF")
        cuadruplo_temporal.set_operando1(resultado)
        cuadruplos.append(cuadruplo_temporal)
        print(cont)
        cont += 1
        pila_saltos.append(cont-1)
        

def p_seen_Cycle(p):
    'seen_Cycle : '
    global pila_operandos
    global cuadruplo_temporal
    global cuadruplos
    global cont
    global pila_saltos
    cuadruplo_temporal = Cuadruplo()
    falso = pila_saltos.pop()
    retorno = pila_saltos.pop()
    cuadruplo_temporal.set_operador("goto")
    cuadruplo_temporal.set_resultado(retorno)
    cuadruplos.append(cuadruplo_temporal)
    print(cont)
    cont += 1
    cuadruplos[falso].set_resultado(cont)

def p_asignacion(p):
    '''
      asignacion : ID seen_Id EQUAL seen_Equals expresion DEL seen_Asignacion
    '''
def p_seen_Asignacion(p):
    'seen_Asignacion : '
    global pila_operadores
    global pila_operandos
    global cuadruplo_temporal
    global cuadruplos
    global cont
    global directorio_temporales
    global directorio_constantes
    global directorio_variables_referenciadas_a_memoria_raiz
    if pila_operadores:
            cuadruplo_temporal = Cuadruplo()
            operando1 = pila_operandos.pop()
            variable_almacen = pila_operandos.pop()
            op2 = verifica_existencia_variable(variable_almacen)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                if cubo_combinaciones[op2['tipo']][op1['tipo']]['='] == 'error':
                        print("NO SE PUEDEN COMBINAR ESOS TIPOS ASIGNACION: ", variable_almacen, op2, operando1, directorio_temporales[operando1])
                else:
                    cuadruplo_temporal.set_operador(pila_operadores.pop())
                    cuadruplo_temporal.set_operando1(operando1)
                    cuadruplo_temporal.set_operando2("null")
                    cuadruplo_temporal.set_resultado(variable_almacen)
                    cuadruplos.append(cuadruplo_temporal)
                    print(cont)
                    cont += 1

            elif op1:
                print("ERROR: NO EXISTE ESTA VARIABLE ALMACEN: ", variable_almacen)
            else:
                print("ERROR: NO EXISTE LA VARIABLE QUE QUIERE ASIGNARSE ", operando1)
                


def p_seen_Equals(p):
    'seen_Equals : '
    global pila_operadores
    pila_operadores.append(p[-1])
    

def p_seen_Id(p):
    'seen_Id : '
    global pila_operandos
    global directorio_variables_referenciadas_a_memoria_raiz
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
      condicion : IF LPARENTH expresion RPARENTH seen_Then bloque condicion_else seen_Condicion
    '''

def p_seen_Then(p):
    'seen_Then : '
    global pila_operandos
    global cuadruplo_temporal
    global pila_saltos
    global cont
    global cuadruplos
    if(True):
        cuadruplo_temporal = Cuadruplo()
        resultado = pila_operandos.pop()
        cuadruplo_temporal.set_operador("GotoF")
        cuadruplo_temporal.set_operando1(resultado)
        cuadruplos.append(cuadruplo_temporal)
        print(cont)
        cont += 1
        pila_saltos.append(cont-1)
        

def p_seen_Condicion(p):
    'seen_Condicion : '
    global pila_saltos
    global cont
    global cuadruplos
    fin = pila_saltos.pop()
    cuadruplos[fin].set_resultado(cont)
    #print(cont)
    #cont += 1
    
    

def p_condicion_else(p):
    '''
      condicion_else : ELSE seen_Else bloque
                     | empty
    '''

def p_seen_Else(p):
    'seen_Else : '
    global cuadruplo_temporal
    global pila_saltos
    global cont
    global cuadruplos
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("goto")
    cuadruplos.append(cuadruplo_temporal)
    print(cont)
    cont += 1
    falso = pila_saltos.pop()
    cuadruplos[falso].set_resultado(cont)
    pila_saltos.append(cont-1)    
    

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
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global directorio_temporales
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '==' or topePila == '<>' or topePila == '>' or topePila == '<':
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador(pila_operadores.pop())
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            #print("COMPARACION: ",operando2, operando1)
            op2 = verifica_existencia_variable(operando2)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                #print("ES AQUI",op2['tipo'],"  ", op1['tipo'])
                if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == 'error':
                    print("NO SE PUEDEN COMBINAR ESTOS TIPOS RELACIONAL", op2, op1)
                else:
                    cuadruplo_temporal.set_operando2(operando2)
                    cuadruplo_temporal.set_operando1(operando1)
                    nombre_temporal = 't' + str(identificadorTemporal)
                    cuadruplo_temporal.set_resultado(nombre_temporal)
                    cuadruplos.append(cuadruplo_temporal)
                    identificadorTemporal += 1
                    print(cont)
                    cont += 1
                    pila_operandos.append(cuadruplo_temporal.get_resultado())
                    directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':''}
            else:
                if not(op2):
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando2)
                else:
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando1)

def p_exp(p):
    '''
     exp : termino seen_Termino exp_aux
    '''

def p_seen_Termino(p):
    'seen_Termino : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global directorio_temporales
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '+' or topePila == '-':
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador(pila_operadores.pop())
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            #print('(', operador, operando1, operando2, resultado, ')')
            #print("SUM O REST: ",operando2,operando1)
            op2 = verifica_existencia_variable(operando2)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == 'error':
                    print("NO SE PUEDEN COMBINAR ESTOS TIPOS TERMINO", op2, op1)
                else:
                    cuadruplo_temporal.set_operando2(operando2)
                    cuadruplo_temporal.set_operando1(operando1)
                    nombre_temporal = 't' + str(identificadorTemporal)
                    cuadruplo_temporal.set_resultado(nombre_temporal)
                    cuadruplos.append(cuadruplo_temporal)
                    identificadorTemporal += 1
                    print(cont)
                    cont += 1
                    pila_operandos.append(cuadruplo_temporal.get_resultado())
                    directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':''}
            else:
                if not(op2):
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando2)
                else:
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando1)
            
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
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global directorio_temporales
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '*' or topePila == '/':
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador(pila_operadores.pop())
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            #print('(', operador, operando1, operando2, resultado, ')')
            #print("MULT O DIV: ",operando2, operando1)
            op2 = verifica_existencia_variable(operando2)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == 'error':
                    print("NO SE PUEDEN COMBINAR ESTOS TIPOS FACTOR". op2, op1)
                else:
                    cuadruplo_temporal.set_operando2(operando2)
                    cuadruplo_temporal.set_operando1(operando1)
                    nombre_temporal = 't' + str(identificadorTemporal)
                    cuadruplo_temporal.set_resultado(nombre_temporal)
                    cuadruplos.append(cuadruplo_temporal)
                    print(cont)
                    cont += 1
                    identificadorTemporal += 1
                    pila_operandos.append(cuadruplo_temporal.get_resultado())
                    directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':''}                    
            else:
                if not(op2):
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando2)
                else:
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando1)

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
    
def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        return False
    return True

def return_type(s):
    if type(s) is float:
        return 'float'
    else:
        return 'int'

def verifica_existencia_variable(s):
    global directorio_variables_referenciadas_a_memoria_temporal
    global directorio_variables_referenciadas_a_memoria_raiz
    global directorio_constantes
    global directorio_temporales
    if s in directorio_variables_referenciadas_a_memoria_temporal:
        return directorio_variables_referenciadas_a_memoria_temporal[s]
    elif s in directorio_variables_referenciadas_a_memoria_raiz['globales']['variables']:
        return directorio_variables_referenciadas_a_memoria_raiz['globales']['variables'][s]
    elif s in directorio_temporales:
        return directorio_temporales[s]
    elif is_number(s):
        directorio_constantes[s] = {'tipo': return_type(s),'dir_virtual':''}
        return directorio_constantes[s]
    else:
        return False
    

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
    print("Nivel A------> ", a)
    if a == "globales":
        for b in directorio_variables_referenciadas_a_memoria_raiz[a]:
            if b != "variables":
                print("\tNivel B------> ", b, " : ", directorio_variables_referenciadas_a_memoria_raiz[a][b])
            else:
                print("\tNivel B------> ", b)
                for c in directorio_variables_referenciadas_a_memoria_raiz[a][b]:
                    print("\t\tNivel C------> ", c ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c])
    else:
        for b in directorio_variables_referenciadas_a_memoria_raiz[a]:
            if b != "variables":
                print("\tNivel B------> ", b, " : ", directorio_variables_referenciadas_a_memoria_raiz[a][b])
            else:
                print("\tNivel B------> ", b)
                for c in directorio_variables_referenciadas_a_memoria_raiz[a][b]:
                    if c != "referencia_Globales":
                        print("\t\tNivel C------> ", c ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c])
                    else:
                        print("\t\tNivel C------> ", c)
                        for d in directorio_variables_referenciadas_a_memoria_raiz[a][b][c]:
                            if d != "variables":
                                print("\t\t\tNivel D------> ", d, " : " ,directorio_variables_referenciadas_a_memoria_raiz[a][b][c][d])
                            else:
                                print("\t\t\tNivel D------> ", d)
                                for e in directorio_variables_referenciadas_a_memoria_raiz[a][b][c][d]:
                                    print("\t\t\t\tNivel E------> ", e ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c][d][e])
    

##for key,val in directorio_variables_referenciadas_a_memoria_raiz.items():
##   print(key, "=>", val)

print()
print("----------------------------------------------------")
print("||                Cuadruplos                     ||")
print("----------------------------------------------------")
print()

indice = 0
for a in cuadruplos:
    print(indice,'( ', a.get_operador(),', ', a.get_operando1(),', ', a.get_operando2(),', ', a.get_resultado(),' )')
    indice += 1
print(cont)
##z = cuadruplos.pop(0)
##
##print("------------")
##print('( ', z.get_operador(),', ', z.get_operando1(),', ', z.get_operando2(),', ', z.get_resultado(), ' )')
##print("------------")
##for a in cuadruplos:
##    print('( ', a.get_operador(),', ', a.get_operando1(),', ', a.get_operando2(),', ', a.get_resultado(), ' )')
##
##print("------------")
##cuadruplos.insert(0, z)
##for a in cuadruplos:
##    print('( ', a.get_operador(),', ', a.get_operando1(),', ', a.get_operando2(),', ', a.get_resultado(), ' )')
##


## ---------------------------------------------------------------------------------------------
## Ejemplos de busquedas
## print(directorio_variables_referenciadas_a_memoria_raiz["main"]["variables"]["referencia_Globales"]["variables"]["dos"])
## ---------------------------------------------------------------------------------------------
##


                    
