#-----------------------------------
# Jose Miguel Rady  920096
# Luis Ordaz        919790
#-----------------------------------
# Orientacion obtenida de la documentacion oficial de python
# http://www.dabeaz.com/ply/example.html

# Importa el modulo de PLY a ser utilizado para generar el analizador
# sintactico (parser)
from Classes import *
from VM import *
import logging
import ply.yacc as yacc


# Importa los tokens generados por el analizador lexico (Esto es requerido)
from funpiling_lexer import tokens

# Declaracion de nuestras estructuras de datos 
# Cubo semantico que define las operaciones que pueden ser aplicadas a determinados tipos
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

# Variables globales
# Diccionarios 
directorio_raiz_procedimientos = {} 
directorio_constantes = {}
directorio_temporales = {}
directorio_recursion = {}
directorio_variables_de_procs = {} 
directorio_variables_referenciadas_a_memoria_raiz = {} 
directorio_variables_referenciadas_a_memoria_temporal = {} 

# Cuadruplo y maquina virtual
cuadruplo_temporal = Cuadruplo()
maquina_virtual = VM()

# Listas 
variables_actuales = [] 
tipo_funcion = [] 
funcion_actual_trabajando = [] 
cuadruplos = []
pila_operadores = []
pila_operandos = []
pila_saltos = []
pila_salto_main = []
nombreParametro = []

# Strings
parametros_referenciados_a_memoria_temporal = ""
nombreScope = ""
tipoParametro = ""
tipoParametroLlamada = ""
nombreFuncionLlamada = ""

# Banderas
sonVariablesGlobales = 1

# Offset y direcciones
dirInicioFuncion = 0
offsetGlobalesEnteras = 1
offsetGlobalesFloats = 100
offsetGlobalesBool = 200
offsetGlobalesString = 300
offsetLocalesEnteras = 1000
offsetLocalesFloats = 1100
offsetLocalesBool = 1200
offsetLocalesString = 1300
offsetConstantesEnteras = 200
offsetConstantesFlotantes = 250
offsetAvailEnteras = 2000
offsetAvailFlotantes = 2100
offsetAvailBool = 2200
offsetAvailString = 2300

# Contadores
cont = 0
identificadorTemporal = 1
contador_de_parametros = 0
contador_de_parametros_llamada = 0
contador_de_ints_locales = 0
contador_de_floats_locales = 0
contador_de_bool_locales = 0
contador_de_string_locales = 0
contador_de_ints_globales = 0
contador_de_floats_globales = 0
contador_de_bool_globales = 0
contador_de_string_globales = 0

# Funcion que permite regresar las variables a sus valores originales
def resetVariables():
    global offsetLocalesEnteras 
    global offsetLocalesFloats
    global offsetLocalesBool
    global offsetLocalesString
    global offsetAvailBool
    global offsetAvailString
    global offsetAvailEnteras
    global offsetAvailFlotantes
    offsetLocalesEnteras = 1000
    offsetLocalesFloats = 1100
    offsetLocalesBool = 1200
    offsetLocalesString = 1300
    offsetAvailEnteras = 2000
    offsetAvailFlotantes = 2100
    offsetAvailBool = 2200
    offsetAvailString = 2300

# Funcion que permite regresar las estructuras a sus valores originales
def resetEstructuras():
    global directorio_temporales
    global directorio_variables_referenciadas_a_memoria_temporal
    global directorio_variables_de_procs
    global parametros_referenciados_a_memoria_temporal
    global nombreParametro
    directorio_temporales = {}
    directorio_variables_referenciadas_a_memoria_temporal = {}
    directorio_variables_de_procs = {}
    parametros_referenciados_a_memoria_temporal = ""
    nombreParametro = []

# Funcion que permite regresar los contadores locales a sus valores originales
def resetContadoresLocales():
    global contador_de_ints_locales 
    global contador_de_floats_locales 
    global contador_de_bool_locales 
    global contador_de_string_locales 
    contador_de_ints_locales = 0
    contador_de_floats_locales = 0
    contador_de_bool_locales = 0
    contador_de_string_locales = 0
    
# Funcion que permite regresar los contadores globales a sus valores originales
def resetContadoresGlobales():
    global contador_de_ints_globales
    global contador_de_floats_globales
    global contador_de_bool_globales 
    global contador_de_string_globales 
    contador_de_ints_globales = 0
    contador_de_floats_globales = 0
    contador_de_bool_globales = 0
    contador_de_string_globales = 0
    
    

# --------------------Analizador Sintactico-------------------------
# Declaraciones de las diferentes reglas empleadas para generar las
# diferentes producciones del lenguaje. La primera produccion debe ser
# aquella considerada como la produccion inicial

# Regla que permite establecer los tokens y no terminales de un programa
def p_programa(p):
    '''programa : vars_globales seen_Vars_Globales funcion MAIN seen_Main bloque seen_Programa 
    '''

# Regla que permite actualizar el directorio de variables locales del main en
# el diccionario raiz de procedimientos y agregarle una referencia a las variables globales
def p_seen_Programa(p):
    'seen_Programa : '
    global nombreScope
    global directorio_variables_referenciadas_a_memoria_raiz 
    global contador_de_ints_locales
    global contador_de_floats_locales
    global contador_de_ints_globales
    global contador_de_floats_globales
    global directorio_temporales
    global directorio_constantes
   
    nombreScope = "main"
    directorio_variables_referenciadas_a_memoria_temporal["referencia_Globales"] = directorio_variables_referenciadas_a_memoria_raiz["globales"]
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["variables"] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["temporales"] = directorio_temporales
    directorio_variables_referenciadas_a_memoria_raiz['globales']['constantes'] = directorio_constantes
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["size"] = {'int':contador_de_ints_locales, 'float':contador_de_floats_locales, 'bool': contador_de_bool_locales, 'string': contador_de_string_locales}
    resetContadoresLocales()
    resetVariables()
    resetEstructuras()

# Regla utilizada para permitir la declaracion de multiples variables globales
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

# Regla que permite iniciar con el registro de las variables del main y genera el salto inicial para
# la generacion del primer cuadruplo
def p_seen_Main(p):
    'seen_Main : '
    global parametros_referenciados_a_memoria_temporal
    global cont
    global cuadruplos
    global nombreParametro
    
    resetVariables()
    directorio_variables_referenciadas_a_memoria_temporal = {}
    parametros_referenciados_a_memoria_temporal = ""
    nombreParametro = []
    inicio = pila_saltos.pop()
    cuadruplos[inicio].set_resultado(cont)
    
# Regla que permite actualizar el directorio de variables globales en el diccionario
# raiz de procedimientos
def p_seen_Vars_Globales(p):
    'seen_Vars_Globales : '
    global sonVariablesGlobales
    global nombreScope
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global contador_de_ints_globales
    global contador_de_floats_globales
    global contador_de_bool_globales
    global contador_de_string_globales
    
    nombreScope = "globales"
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["variables"] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["size"] = {'int':contador_de_ints_globales, 'float':contador_de_floats_globales, 'bool' : contador_de_bool_globales, 'string:': contador_de_string_globales}
    resetEstructuras()
    resetContadoresGlobales()
    sonVariablesGlobales = 0
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("goto")
    cuadruplos.append(cuadruplo_temporal)
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
        global offsetGlobalesBool
        global offsetGlobalesString
        global offsetLocalesEnteras 
        global offsetLocalesFloats
        global offsetLocalesBool
        global offsetLocalesString
        global nombreScope
        global directorio_variables_referenciadas_a_memoria_raiz
        global directorio_variables_referenciadas_a_memoria_temporal
        global contador_de_ints_locales
        global contador_de_floats_locales
        global contador_de_bool_locales
        global contador_de_string_locales
        global contador_de_ints_globales 
        global contador_de_floats_globales
        global contador_de_bool_globales
        global contador_de_string_globales

        if (p[-1] in directorio_variables_de_procs):
                directorio_variables_de_procs[p[-1]]['variables'].extend(variables_actuales)
        else:
            directorio_variables_de_procs[p[-1]] = {'variables':variables_actuales}
        variables_actuales = []
        if sonVariablesGlobales == 1:
            for a in directorio_variables_de_procs:
                if a == "int":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesEnteras, 'tipo':a, 'valor': 0}
                            offsetGlobalesEnteras += 1
                            contador_de_ints_globales+= 1
                elif a == "float":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesFloats, 'tipo':a, 'valor':0}
                            offsetGlobalesFloats += 1
                            contador_de_floats_globales += 1
                elif a == "bool":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesBool, 'tipo':a, 'valor':True}
                            offsetGlobalesBool += 1
                            contador_de_bool_globales += 1
                elif a == "string":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetGlobalesString, 'tipo':a, 'valor':""}
                            offsetGlobalesString += 1
                            contador_de_string_globales += 1
                    
        else:
            for a in directorio_variables_de_procs:
                if a == "int":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetLocalesEnteras, 'tipo':a}
                            offsetLocalesEnteras += 1
                            contador_de_ints_locales +=1
                elif a == "float":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetLocalesFloats, 'tipo':a}
                            offsetLocalesFloats += 1
                            contador_de_floats_locales += 1
                elif a == "bool":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetLocalesBool, 'tipo':a}
                            offsetLocalesBool += 1
                            contador_de_bool_locales += 1
                elif a == "string":
                    for b in directorio_variables_de_procs[a]['variables']:
                        if (b not in directorio_variables_referenciadas_a_memoria_temporal):
                            directorio_variables_referenciadas_a_memoria_temporal[b] = {'dir_virtual': offsetLocalesString, 'tipo':a}
                            offsetLocalesString += 1
                            contador_de_string_locales += 1

    elif p[-2] == '(' or p[-2] == ',':
        global tipoParametro
        tipoParametro = p[-1]

    else:
        global tipo_funcion
        tipo_funcion.append(p[-1])
            
# Regla que permite actualizar el directorio de variables locales de cada funcion en
# el diccionario raiz de procedimientos y agregarle una referencia a las variables globales
def p_seen_Funcion(p):
    'seen_Funcion : '
    global directorio_raiz_procedimientos
    global directorio_variables_referenciadas_a_memoria_raiz 
    global contador_de_parametros
    global tipo_funcion
    global nombreScope
    global contador_de_ints_locales
    global contador_de_floats_locales
    global contador_de_bool_locales
    global contador_de_string_locales
    global contador_de_ints_globales
    global contador_de_floats_globales
    global cont
    global cuadruplos
    global cuadruplo_temporal
    global dirInicioFuncion
    global nombreParametro
    global pila_operandos

    nombreScope = p[-6]
    directorio_variables_referenciadas_a_memoria_temporal["referencia_Globales"] = directorio_variables_referenciadas_a_memoria_raiz["globales"]
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope] = {}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["variables"] = directorio_variables_referenciadas_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["temporales"] = directorio_temporales
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["parametros"] = parametros_referenciados_a_memoria_temporal
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["nombre_parametros"] = nombreParametro
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["size"] = {'int':contador_de_ints_locales, 'float':contador_de_floats_locales, 'bool': contador_de_bool_locales, 'string': contador_de_string_locales}
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["tipo"] = tipo_funcion.pop()
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["valor"] = 0
    directorio_variables_referenciadas_a_memoria_raiz[nombreScope]["cuadruplo_inicial"] = dirInicioFuncion
    resetVariables()
    resetContadoresLocales()
    resetEstructuras()
    contador_de_parametros = 0
    cuadruplo_temporal = Cuadruplo()
    if directorio_variables_referenciadas_a_memoria_raiz[nombreScope]['tipo'] == "float" or directorio_variables_referenciadas_a_memoria_raiz[nombreScope]['tipo'] == "int" or directorio_variables_referenciadas_a_memoria_raiz[nombreScope]['tipo'] == "bool" or directorio_variables_referenciadas_a_memoria_raiz[nombreScope]['tipo'] == "string":
        cuadruplo_temporal.set_operador("ret")
    else:
        cuadruplo_temporal.set_operador("ret")
    cuadruplos.append(cuadruplo_temporal)
    cont += 1

# Regla empleada para las producciones vacias
def p_empty(p):
    'empty : '
    pass

# Regla que identifica los contenidos de un bloque
def p_bloque(p):
    '''
      bloque : LBRACE bloque_estatuto RBRACE
    '''
# Regla que indica que un bloque puede tener varios estatutos
def p_bloque_estatuto(p):
    '''
       bloque_estatuto : estatuto bloque_estatuto
                       | empty
    '''
    
# Regla que identifica los tipos de estatutos aceptados por el lenguaje
def p_estatuto(p):
    '''
      estatuto : asignacion
               | llamada_funcion
               | condicion
               | escritura
               | vars
               | while_loop
               | retorno
    '''

# Regla que identifica los contenidos aceptadas para la declaracion de una funcion
def p_funcion(p):
    '''
      funcion : tipoFuncion ID seenIdDeclaracionFuncion LPARENTH vars_funcion RPARENTH bloque seen_Funcion funcion
              | empty
    '''
    
# Regla que identifica cuando la declaracion de una funcion ha iniciado y actualiza el contexto
def p_seenIdDeclaracionFuncion(p):
    'seenIdDeclaracionFuncion : '
    global nombreScope 
    nombreScope = p[-1]

# Regla que identifica a las variables declaradas dentro de una funcion
def p_vars_funcion(p):
    '''
      vars_funcion : tipo ID seen_Param vars_funcion_aux
                   | empty
    '''
    global dirInicioFuncion
    global cont
    dirInicioFuncion = cont

# Regla que permite la declaracion de multiples variables en una linea
def p_vars_funcion_aux(p):
    '''
      vars_funcion_aux : COMMA tipo ID seen_Param vars_funcion_aux
                       | empty
    '''

# Regla que identifica los parametros y sus tipos declarados en la funcion y actualiza las estructuras correspondientes
def p_seen_Param(p):
    'seen_Param : '
    global contador_de_ints_locales
    global contador_de_floats_locales
    global contador_de_bool_locales
    global contador_de_string_locales
    global contador_de_parametros
    global tipoParametro
    global nombreParametro
    global directorio_variables_referenciadas_a_memoria_temporal
    global parametros_referenciados_a_memoria_temporal
    global offsetLocalesFloats
    global offsetLocalesEnteras
    global offsetLocalesString
    global offsetLocalesBool
    
    idParametro = p[-1]
    if tipoParametro == "int":
        if idParametro not in directorio_variables_referenciadas_a_memoria_temporal:
            directorio_variables_referenciadas_a_memoria_temporal[idParametro] = {'tipo':tipoParametro, 'dir_virtual':offsetLocalesEnteras, 'valor':0}
            offsetLocalesEnteras += 1
            contador_de_ints_locales += 1
            if parametros_referenciados_a_memoria_temporal == "":
                parametros_referenciados_a_memoria_temporal = tipoParametro
            else:
                parametros_referenciados_a_memoria_temporal += ", " + tipoParametro
            nombreParametro.append(idParametro)
    elif tipoParametro == "float":
        if idParametro not in directorio_variables_referenciadas_a_memoria_temporal:
            directorio_variables_referenciadas_a_memoria_temporal[idParametro] = {'tipo':tipoParametro, 'dir_virtual': offsetLocalesFloats, 'valor':0}
            offsetLocalesFloats += 1
            contador_de_floats_locales += 1
            if parametros_referenciados_a_memoria_temporal == "":
                parametros_referenciados_a_memoria_temporal = tipoParametro
            else:
                parametros_referenciados_a_memoria_temporal += ", " + tipoParametro
            nombreParametro.append(idParametro)
    elif tipoParametro == "bool":
        if idParametro not in directorio_variables_referenciadas_a_memoria_temporal:
            directorio_variables_referenciadas_a_memoria_temporal[idParametro] = {'tipo':tipoParametro, 'dir_virtual': offsetLocalesBool, 'valor':True}
            offsetLocalesBool += 1
            contador_de_bool_locales += 1
            if parametros_referenciados_a_memoria_temporal == "":
                parametros_referenciados_a_memoria_temporal = tipoParametro
            else:
                parametros_referenciados_a_memoria_temporal += ", " + tipoParametro
            nombreParametro.append(idParametro)
    elif tipoParametro == "string":
        if idParametro not in directorio_variables_referenciadas_a_memoria_temporal:
            directorio_variables_referenciadas_a_memoria_temporal[idParametro] = {'tipo':tipoParametro, 'dir_virtual': offsetLocalesString, 'valor':""}
            offsetLocalesString += 1
            contador_de_string_locales += 1
            if parametros_referenciados_a_memoria_temporal == "":
                parametros_referenciados_a_memoria_temporal = tipoParametro
            else:
                parametros_referenciados_a_memoria_temporal += ", " + tipoParametro
            nombreParametro.append(idParametro)
    contador_de_parametros = contador_de_parametros + 1


# Regla que identifica la declaracion apropiada del ciclo while
def p_while_loop(p):
    '''
      while_loop : WHILE seen_While LPARENTH expresion RPARENTH seen_Do bloque seen_Cycle
    '''

# Regla que registra el salto del incicio del ciclo while
def p_seen_While(p):
    'seen_While : '
    global pila_saltos
    pila_saltos.append(cont)

# Regla que genera el gotof del ciclo
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
        cont += 1
        pila_saltos.append(cont-1)       

# Regla que rellena con goto el salto necesario para el ciclo 
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
    cont += 1
    cuadruplos[falso].set_resultado(cont)

# Regla que identifica la sintaxis necesaria para los retornos de una funcion    
def p_retorno(p):
    '''retorno : RETURN expresion seenExpresionRetorno DEL
    '''

# Regla que genera el cuadruplo necesario para el valor de retorno de la funcion
def p_seenExpresionRetorno(p):
    'seenExpresionRetorno : '
    global cuadruplo_temporal
    global cont
    global cuadruplos
    global pila_operandos
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("retorno")
    cuadruplo_temporal.set_operando1(pila_operandos[len(pila_operandos)-1])
    cuadruplos.append(cuadruplo_temporal)
    cont += 1

# Regla que identifica la sintaxis necesaria para realizar una asignacion
def p_asignacion(p):
    '''
      asignacion : ID seen_Id EQUAL seen_Equals expresion DEL seen_Asignacion
    '''

# Regla que identifica que se ha visto una asignacion y genera el cuadruplo correspondiente
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
                        print("NO SE PUEDEN COMBINAR ESOS TIPOS ASIGNACION: ", variable_almacen, op2['tipo'], operando1, op1['tipo'])
                else:
                    cuadruplo_temporal.set_operador(pila_operadores.pop())
                    cuadruplo_temporal.set_operando1(operando1)
                    cuadruplo_temporal.set_resultado(variable_almacen)
                    cuadruplos.append(cuadruplo_temporal)
                    cont += 1

            elif op1:
                print("ERROR: NO EXISTE ESTA VARIABLE ALMACEN: ", variable_almacen)
            else:
                print("ERROR: NO EXISTE LA VARIABLE QUE QUIERE ASIGNARSE ", operando1)                

# Regla que identifica un signo de igual y actualiza la pila de operadores
def p_seen_Equals(p):
    'seen_Equals : '
    global pila_operadores
    pila_operadores.append(p[-1])
    
# Regla que identifica un id y actualiza la pila de operandos
def p_seen_Id(p):
    'seen_Id : '
    global pila_operandos
    pila_operandos.append(p[-1])
    

# Regla que identifica una llamada a funcion del tipo void
def p_llamada_funcion(p):
    '''
      llamada_funcion : ID LPARENTH seenIdFuncion seenParenthFuncion llamada_funcion_expresion RPARENTH DEL seenLlamadaFuncion
    '''

# Regla que identifica una llamada a funcion con retorno
def p_llamada_funcion2(p):
    '''
      llamada_funcion2 : LPARENTH seenIdFuncion2 seenParenthFuncion llamada_funcion_expresion RPARENTH seenLlamadaFuncion
    '''
    
# Regla que identifica que se ha llamado a una funcion y revisa que los parametros sean correctos
def p_seenLlamadaFuncion(p):
    'seenLlamadaFuncion : '
    global tipoParametroLlamada
    global nombreFuncionLlamada
    global directorio_variables_referenciadas_a_memoria_raiz
    global cuadruplo_temporal
    global cont
    global pila_operadores
    global parametros_referenciados_a_memoria_temporal
    global nombreScope
    global dirInicioFuncion

    if nombreFuncionLlamada in directorio_variables_referenciadas_a_memoria_raiz.keys():
        if tipoParametroLlamada == directorio_variables_referenciadas_a_memoria_raiz[nombreFuncionLlamada]['parametros']:
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador("gosub")
            cuadruplo_temporal.set_operando1(nombreFuncionLlamada)
            cuadruplo_temporal.set_resultado(directorio_variables_referenciadas_a_memoria_raiz[nombreFuncionLlamada]['cuadruplo_inicial'])
            cuadruplos.append(cuadruplo_temporal)
            cont += 1
            pila_operadores.reverse()
            if pila_operadores.count("(") > 0:
                pila_operadores.remove("(")
            pila_operadores.reverse()

    elif nombreFuncionLlamada == nombreScope:
        if tipoParametroLlamada == parametros_referenciados_a_memoria_temporal:
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador("gosub")
            cuadruplo_temporal.set_operando1(nombreFuncionLlamada)
            cuadruplo_temporal.set_resultado(dirInicioFuncion)
            cuadruplos.append(cuadruplo_temporal)
            cont += 1
            pila_operadores.reverse()
            if pila_operadores.count("(") > 0:
                pila_operadores.remove("(")
            pila_operadores.reverse()
        
    else:
        print("La funcion", nombreFuncionLlamada, "espera como parametros: ", directorio_variables_referenciadas_a_memoria_raiz[nombreFuncionLlamada]['parametros'])

# Regla que identifica el nombre de la funcion tipo void que sera llamada
def p_seenIdFuncion(p):
    'seenIdFuncion : '
    global directorio_variables_referenciadas_a_memoria_raiz
    global nombreFuncionLlamada
    global directorio_variables_referenciadas_a_memoria_temporal
    global nombreScope
    if p[-2] in directorio_variables_referenciadas_a_memoria_raiz.keys():
        nombreFuncionLlamada = p[-2]
    elif p[-2] == nombreScope:
        nombreFuncionLlamada = p[-2]
    else:
        print("La funcion", p[-2], "no fue declarada")

# Regla que identifica el nombre de la funcion con retorno que sera llamada
def p_seenIdFuncion2(p):
    'seenIdFuncion2 : '
    global directorio_variables_referenciadas_a_memoria_raiz
    global nombreFuncionLlamada
    global pila_operandos
    global pila_operadores
    global directorio_variables_referenciadas_a_memoria_temporal
    global nombreScope
    if p[-2] in directorio_variables_referenciadas_a_memoria_raiz.keys():
        nombreFuncionLlamada = p[-2]
        pila_operadores.append("(")
        pila_operandos.append(nombreFuncionLlamada)
    elif p[-2] == nombreScope:
        nombreFuncionLlamada = p[-2]
        pila_operadores.append("(")
        pila_operandos.append(nombreFuncionLlamada) 
    else:
        print(nombreScope)
        print(p[-2])
        print("La funcion", p[-2], "no fue declarada")

# Regla que identifica que se ha visto el parentesis de la funcion y genera el cuadruplo del era
def p_seenParenthFuncion(p):
    'seenParenthFuncion : '
    global cuadruplo_temporal
    global cont
    global cuadruplos
    global tipoParametroLlamada
    global nombreFuncionLlamada
    global contador_de_parametros_llamada
    
    tipoParametroLlamada = ""
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("era")
    cuadruplo_temporal.set_operando1(nombreFuncionLlamada)
    cuadruplos.append(cuadruplo_temporal)
    contador_de_parametros_llamada = 1
    cont += 1
    
# Regla que identifica la definicion de la expresion que puede ser contenida en los parentesis de la llamada a funcion
def p_llamada_funcion_expresion(p):
    '''
      llamada_funcion_expresion : expresion seenExpresionLlamada llamada_funcion_expresion_aux 
                                | empty
    '''

# Regla que identifica la expresion a ser evaluada para ser utilizada como parametro y actualiza las estructuras pertinentes y genera los cuadruplos de params
def p_seenExpresionLlamada(p):
    'seenExpresionLlamada : '
    global cuadruplo_temporal
    global cont
    global cuadruplos
    global pila_operandos
    global directorio_variables_referenciadas_a_memoria_raiz
    global directorio_variables_referenciadas_a_memoria_temporal
    global nombreParametro
    global nombreFuncionLlamada
    global tipoParametroLlamada
    global contador_de_parametros_llamada

    argumento = pila_operandos.pop()
    
    if argumento in directorio_variables_referenciadas_a_memoria_temporal:
        tipoArgumento = directorio_variables_referenciadas_a_memoria_temporal[argumento]['tipo']
        
    elif argumento in directorio_temporales:
        tipoArgumento = directorio_temporales[argumento]['tipo']
        
    elif argumento in directorio_variables_referenciadas_a_memoria_raiz['globales']['variables']:
        tipoArgumento = directorio_variables_referenciadas_a_memoria_raiz['globales']['variables'][argumento]['tipo']

    else:
        if type(argumento) == int:
            tipoArgumento = "int"

        elif type(argumento) == float:
            tipoArgumento = "float"

        elif type(argumento) == bool:
            tipoArgumento = "bool"

        elif type(argumento) == str:
            tipoArgumento = "string"

    if tipoParametroLlamada == "":
        tipoParametroLlamada = tipoArgumento

    else:
        tipoParametroLlamada = tipoParametroLlamada + ", " + tipoArgumento

    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("param")
    cuadruplo_temporal.set_operando1(argumento)
    if nombreFuncionLlamada in directorio_variables_referenciadas_a_memoria_raiz.keys():
        cuadruplo_temporal.set_operando2(directorio_variables_referenciadas_a_memoria_raiz[nombreFuncionLlamada]['nombre_parametros'][contador_de_parametros_llamada - 1])
    else:
        cuadruplo_temporal.set_operando2(nombreParametro[contador_de_parametros_llamada - 1])
    cuadruplo_temporal.set_resultado("param" + str(contador_de_parametros_llamada))
    cuadruplos.append(cuadruplo_temporal)
    cont += 1
  
# Regla que permite que los multiples parametros puedan ser generados a traves de multiples expresiones
def p_llamada_funcion_expresion_aux(p):
    '''
      llamada_funcion_expresion_aux : COMMA seenCommaLlamada expresion seenExpresionLlamada llamada_funcion_expresion_aux
                                    | empty
    '''
# Regla que identifica el numero de parametros de la funcion a ser llamada
def p_seenCommaLlamada(p):
    'seenCommaLlamada : '
    global contador_de_parametros_llamada
    contador_de_parametros_llamada += 1

# Regla que identifica la sintaxis para un estatuto condicional
def p_condicion(p):
    '''
      condicion : IF LPARENTH expresion RPARENTH seen_Then bloque condicion_else seen_Condicion
    '''
# Regla que identifica la existencia de un if
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
        #print(cont)
        cont += 1
        pila_saltos.append(cont-1)
        
# Regla que identifica la existencia de un estatuto else
def p_seen_Condicion(p):
    'seen_Condicion : '
    global pila_saltos
    global cont
    global cuadruplos
    fin = pila_saltos.pop()
    cuadruplos[fin].set_resultado(cont)
    
    
# Regla que identifica la sintaxis apropiada para el else
def p_condicion_else(p):
    '''
      condicion_else : ELSE seen_Else bloque
                     | empty
    '''
# Regla que genera el goto necesario si la condicion es falsa
def p_seen_Else(p):
    'seen_Else : '
    global cuadruplo_temporal
    global pila_saltos
    global cont
    global cuadruplos
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("goto")
    cuadruplos.append(cuadruplo_temporal)
    cont += 1
    falso = pila_saltos.pop()
    cuadruplos[falso].set_resultado(cont)
    pila_saltos.append(cont-1)    
    
# Regla que identifica la sintaxis apropiada para los estatutos de impresion
def p_escritura(p):
    '''
      escritura : PRINT LPARENTH expresion seen_Print RPARENTH DEL
    '''
# Regla que genera el cuadruplo necesario para un print
def p_seen_Print(p):
    'seen_Print : '
    global cuadruplo_temporal
    global cont
    global cuadruplos
    global pila_operandos
    cuadruplo_temporal = Cuadruplo()
    cuadruplo_temporal.set_operador("print")
    cuadruplo_temporal.set_resultado(pila_operandos[len(pila_operandos)-1])
    cuadruplos.append(cuadruplo_temporal)
    cont += 1

# Regla que identifica sintaxis apropiada para una declaracion de variables
def p_vars(p):
    '''
      vars : VAR ID seen_Vars vars_aux COLON tipo DEL
      
    '''

# Regla que permite declarar multiples variables del mismo tipo en una linea 
def p_vars_aux(p):
    '''
      vars_aux : COMMA ID seen_Vars vars_aux
               | empty
    '''

# Regla que identifica los diferentes tipos de variables
def p_tipo(p):
    '''
      tipo : INTEGER_ID seen_Tipo
           | FLOAT_ID seen_Tipo
           | STRING_ID seen_Tipo
           | BOOL_ID seen_Tipo

    '''

# Regla que identifica los diferentes tipos de funciones
def p_tipoFuncion(p):
    '''
      tipoFuncion : INTEGER_ID seen_Tipo
           | FLOAT_ID seen_Tipo
           | STRING_ID seen_Tipo
           | BOOL_ID seen_Tipo
           | VOID seen_Tipo

    '''

# Regla que identifica la sintaxis de una expresion
def p_expresion(p):
    '''
      expresion : exp
                | exp LTHAN seen_OperadorRelacional exp seen_Relacional
                | exp GTHAN seen_OperadorRelacional exp seen_Relacional
                | exp DIFF seen_OperadorRelacional exp seen_Relacional
                | exp SAME seen_OperadorRelacional exp seen_Relacional
    '''

# Regla que identifica que se ha visto un operador relacional
def p_seen_OperadorRelacional(p):
    'seen_OperadorRelacional : '
    global pila_operadores
    pila_operadores.append(p[-1])

# Regla que se asegura de que la operacion relacional sea valida y genera el cuadruplo resultante
def p_seen_Relacional(p):
    'seen_Relacional : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global directorio_temporales
    global offsetAvailEnteras
    global offsetAvailFlotantes
    global offsetAvailBool
    global offsetAvailString
    
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '==' or topePila == '<>' or topePila == '>' or topePila == '<':
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador(pila_operadores.pop())
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            op2 = verifica_existencia_variable(operando2)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == 'error':
                    print("NO SE PUEDEN COMBINAR ESTOS TIPOS RELACIONAL", operando2, op2['tipo'], operando1, op1['tipo'])
                else:
                    cuadruplo_temporal.set_operando2(operando2)
                    cuadruplo_temporal.set_operando1(operando1)
                    nombre_temporal = 't' + str(identificadorTemporal)
                    cuadruplo_temporal.set_resultado(nombre_temporal)
                    cuadruplos.append(cuadruplo_temporal)
                    identificadorTemporal += 1
                    cont += 1
                    pila_operandos.append(cuadruplo_temporal.get_resultado())
                    if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "int":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailEnteras, 'valor':0}
                        offsetAvailEnteras += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "float":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailFlotantes, 'valor':0}
                        offsetAvailFlotantes += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "bool":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailBool, 'valor':True}
                        offsetAvailBool += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "string":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailString, 'valor':""}
                        offsetAvailString += 1
                    
            else:
                if not(op2):
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando2)
                else:
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando1)

# Regla que identifica la sintaxis para una exp que permite la creacion de prioridades entre los operadores aritmeticos
def p_exp(p):
    '''
     exp : termino seen_Termino exp_aux
    '''

# Regla que identifica la existencia de una suma o resta y su validez 
def p_seen_Termino(p):
    'seen_Termino : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global directorio_temporales
    global offsetAvailEnteras
    global offsetAvailFlotantes
    global offsetAvailBool
    global offsetAvailString
    
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '+' or topePila == '-':
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador(pila_operadores.pop())
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            op2 = verifica_existencia_variable(operando2)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == 'error':
                    print("NO SE PUEDEN COMBINAR ESTOS TIPOS TERMINO", operando2, op2['tipo'], operando1, op1['tipo'])
                else:
                    cuadruplo_temporal.set_operando2(operando2)
                    cuadruplo_temporal.set_operando1(operando1)
                    nombre_temporal = 't' + str(identificadorTemporal)
                    cuadruplo_temporal.set_resultado(nombre_temporal)
                    cuadruplos.append(cuadruplo_temporal)
                    identificadorTemporal += 1
                    cont += 1
                    pila_operandos.append(cuadruplo_temporal.get_resultado())
                    if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "int":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailEnteras, 'valor': 0}
                        offsetAvailEnteras += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "float":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailFlotantes, 'valor': 0}
                        offsetAvailFlotantes += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "bool":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailBool, 'valor': True}
                        offsetAvailBool += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "string":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailString, 'valor':""}
                        offsetAvailString += 1
            else:
                if not(op2):
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando2)
                else:
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando1)

# Regla que permite multiples sumas y restas por linea 
def p_exp_aux(p):
    '''
      exp_aux : PLUS seen_Plus exp
              | MINUS seen_Minus exp
              | empty
    '''

# Regla que identifica un operador de suma y actualiza la pila de operadores
def p_seen_Plus(p):
    'seen_Plus : '
    global pila_operadores
    pila_operadores.append(p[-1])

# Regla que identifica un operador de resta y actualiza la pila de operadores
def p_seen_Minus(p):
    'seen_Minus : '
    global pila_operadores
    pila_operadores.append(p[-1])

# Regla que identfica la sintaxis necesaria para multiplicaciones y divisiones
def p_termino(p):
    '''
      termino : factor seen_Factor termino_aux
    '''

# Regla que identifica la existencia de una multiplicacion o division y su validez
def p_seen_Factor(p):
    'seen_Factor : '
    global pila_operadores
    global pila_operandos
    global identificadorTemporal
    global cuadruplos
    global cuadruplo_temporal
    global cont
    global directorio_temporales
    global offsetAvailEnteras
    global offsetAvailFlotantes
    global offsetAvailBool
    global offsetAvailString
    
    if pila_operadores and pila_operandos:
        topePila = pila_operadores[-1]
        if topePila == '*' or topePila == '/':
            cuadruplo_temporal = Cuadruplo()
            cuadruplo_temporal.set_operador(pila_operadores.pop())
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            op2 = verifica_existencia_variable(operando2)
            op1 = verifica_existencia_variable(operando1)
            if op2 and op1:
                if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == 'error':
                    print("NO SE PUEDEN COMBINAR ESTOS TIPOS FACTOR", operando2, op2['tipo'], operando1, op1['tipo'])
                else:
                    cuadruplo_temporal.set_operando2(operando2)
                    cuadruplo_temporal.set_operando1(operando1)
                    nombre_temporal = 't' + str(identificadorTemporal)
                    cuadruplo_temporal.set_resultado(nombre_temporal)
                    cuadruplos.append(cuadruplo_temporal)
                    cont += 1
                    identificadorTemporal += 1
                    pila_operandos.append(cuadruplo_temporal.get_resultado())
                    if cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "int":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailEnteras, 'valor':0}
                        offsetAvailEnteras += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "float":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailFlotantes, 'valor':0}
                        offsetAvailFlotantes += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "bool":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailBool, 'valor': True}
                        offsetAvailBool += 1
                    elif cubo_combinaciones[op2['tipo']][op1['tipo']][topePila] == "string":
                        directorio_temporales[nombre_temporal] = {'tipo':cubo_combinaciones[op2['tipo']][op1['tipo']][topePila],'dir_virtual':offsetAvailString, 'valor': ""}
                        offsetAvailString += 1
            else:
                if not(op2):
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando2)
                else:
                    print("ERROR: NO EXISTE ESTA VARIABLE: ", operando1)

# Regla que permite multiples divisiones y multiplicaciones por linea
def p_termino_aux(p):
    '''
      termino_aux : TIMES seen_Times termino
                  | DIVIDE seen_Divide termino
                  | empty
    '''

# Regla que identifica a un operador de multiplicacion y lo agrega a la pila de operadores
def p_seen_Times(p):
    'seen_Times : '
    global pila_operadores
    pila_operadores.append(p[-1])

# Regla que identifica a un operador de division y lo agrega a la pila de operadores
def p_seen_Divide(p):
    'seen_Divide : '
    global pila_operadores
    pila_operadores.append(p[-1])

# Regla que identifica a los elementos atomicos de las operaciones matematicas
def p_factor(p):
    '''
      factor : ID opcion_Id 
             | TRUE seen_Id
             | FALSE seen_Id
             | factor_sign INTEGER seen_Id
             | factor_sign FLOAT seen_Id
             | LPARENTH seen_Leftparenth exp RPARENTH seen_Rightparenth
             | STRING seen_Id
    '''

# Regla que identifica que se ha visto una id en las operaaciones matematicas
def p_opcion_Id(p):
    '''
      opcion_Id : llamada_funcion2
               | seen_Id
    '''
    
# Regla que identifica la existencia de un parentesis y agrega un fondo falso a la pila de operadores
def p_seen_Leftparenth(p):
    'seen_Leftparenth : '
    global pila_operadores
    pila_operadores.append("(")
    
# Regla que remueve el fondo falso de la pila de operadores
def p_seen_Rightparenth(p):
    'seen_Rightparenth : '
    global pila_operadores
    pila_operadores.reverse()
    pila_operadores.remove("(")
    pila_operadores.reverse()
    
# Regla que permite el uso de signos para las variables numericas   
def p_factor_sign(p):
    '''
      factor_sign : PLUS 
                  | MINUS 
                  | empty
    '''
# Funcion que identifica si una variable es numerica (entera, long o flotante)   
def is_number(s):
    try:
        float(s) 
    except ValueError:
        return False
    return True

# Funcion que regresa como string el tipo de una variable
def return_type(s):
    if type(s) is float:
        return 'float'
    elif type(s) is int:
        return 'int'
    elif type (s) is bool:
        return 'bool'
    elif type(s) is str:
        return 'string'
    
# Funcion que identifica la existencia de variables
def verifica_existencia_variable(s):
    global directorio_variables_referenciadas_a_memoria_temporal
    global directorio_variables_referenciadas_a_memoria_raiz
    global directorio_constantes
    global directorio_temporales
    global directorio_recursion
    global nombreScope
    global tipo_funcion

    if s in directorio_variables_referenciadas_a_memoria_temporal:
        return directorio_variables_referenciadas_a_memoria_temporal[s]
    elif s in directorio_variables_referenciadas_a_memoria_raiz['globales']['variables']:
        return directorio_variables_referenciadas_a_memoria_raiz['globales']['variables'][s]
    elif s in directorio_temporales:
        return directorio_temporales[s]
    elif s in directorio_variables_referenciadas_a_memoria_raiz:
        return directorio_variables_referenciadas_a_memoria_raiz[s]
    elif is_number(s):
        directorio_constantes[s] = {'tipo': return_type(s),'dir_virtual':'', 'valor': s}
        return directorio_constantes[s]
    elif s == nombreScope:
        directorio_recursion[s] = {'tipo': tipo_funcion[len(tipo_funcion)-1], 'dir_virtual':'', 'valor':0}
        return directorio_recursion[s]
    else:
        if s=="True" or s=="False":
            s = bool(s)
        directorio_constantes[s] = {'tipo': return_type(s),'dir_virtual':'', 'valor': s}
        return directorio_constantes[s]

# Regla sintactica que identifica un error de sintaxis
def p_error(p):
    print("Syntax error in input!", p)
    
# Funcion que permite imprimir todos los cuadruplos en la lista de cuadruplos
def print_cuadruplos():
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
    input()

# Funcion que permite imprimir a manera de drill in los contenidos de la tabla de variables
def print_tabla_de_variables():
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
                if b != "variables" and b!= "temporales" and b!="constantes":
                    print("\tNivel B------> ", b, " : ", directorio_variables_referenciadas_a_memoria_raiz[a][b])
                else:
                    print("\tNivel B------> ", b)
                    for c in directorio_variables_referenciadas_a_memoria_raiz[a][b]:
                        print("\t\tNivel C------> ", c ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c])
        else:
            for b in directorio_variables_referenciadas_a_memoria_raiz[a]:
                if b != "variables" and b!= "temporales" and b!="constantes":
                    print("\tNivel B------> ", b, " : ", directorio_variables_referenciadas_a_memoria_raiz[a][b])
                else:
                    print("\tNivel B------> ", b)
                    for c in directorio_variables_referenciadas_a_memoria_raiz[a][b]:
                        if c != "referencia_Globales":
                            print("\t\tNivel C------> ", c ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c])
                        else:
                            print("\t\tNivel C------> ", c)
                            for d in directorio_variables_referenciadas_a_memoria_raiz[a][b][c]:
                                if d != "variables" and d != "temporales" and d!= "constantes":
                                    print("\t\t\tNivel D------> ", d, " : " ,directorio_variables_referenciadas_a_memoria_raiz[a][b][c][d])
                                else:
                                    print("\t\t\tNivel D------> ", d)
                                    for e in directorio_variables_referenciadas_a_memoria_raiz[a][b][c][d]:
                                        print("\t\t\t\tNivel E------> ", e ," : ",directorio_variables_referenciadas_a_memoria_raiz[a][b][c][d][e])
    input()
    
    

# Creacion del parser en relacion a las reglas sintacticas generadas
# y a los tokens creados por medio del analizador lexico
parser = yacc.yacc(debug=True)

# Seccion de pruebas obteniendo como entrada un archivo de texto
f = open("VM.txt")
datos = f.read()
print(datos)

# Aplicacion del analizador lexico y sintactico a la entrada
logging.basicConfig(filename='example.log',level=logging.INFO)
log = logging.getLogger('example.log')
result = parser.parse(datos,debug=log)

# Impresion del contenido de cuadruplos y de la tabla de variables
#print_cuadruplos()
#print_tabla_de_variables()

# Invocacion de la maquina virtual e inicio de la ejecucion    
maquina_virtual.set_cuadruplos_y_memoria(cuadruplos, directorio_variables_referenciadas_a_memoria_raiz)
maquina_virtual.start()
