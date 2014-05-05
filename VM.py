from copy import deepcopy
class VM:
    def __init__(self):
        self.cuadruplos = 0

    def set_cuadruplos_y_memoria(self, cuadruplos, memoria):
        self.cuadruplos = cuadruplos
        self.memoria = memoria
        self.indice = self.cuadruplos[0].get_resultado()
        self.scope = "main"
        self.scopePrevio = "main"
        self.indice_pasado = -1
        self.pila_de_ejecucion = []
        self.pila_de_cuadruplo_de_retorno = []
        self.pila_de_valores_de_retorno = []
        self.contadorRecursividad = 1
        self.memoriaTemporal = {}
        self.contadorInicial = 0

    def get_cuadruplos(self):
        return cuadruplos
    
    def print_memoria(self):
        input()
        print()
        print("----------------------------------------------------")
        print("||    Contenidos de nuestras tablas de simbolos   ||")
        print("----------------------------------------------------")
        print()

        for a in self.memoria:
            print("----------------")
            print("Nivel A------> ", a)
            if a == "globales":
                for b in self.memoria[a]:
                    if b != "variables" and b!= "temporales" and b!="constantes":
                        print("\tNivel B------> ", b, " : ", self.memoria[a][b])
                    else:
                        print("\tNivel B------> ", b)
                        for c in self.memoria[a][b]:
                            print("\t\tNivel C------> ", c ," : ",self.memoria[a][b][c])
                            
            elif a == "originales":
                for b in self.memoria[a]:
                    print("\tNivel B------> ", b)
                    for c in self.memoria[a][b]:
                        if c!= "variables" and c!= "temporales" and c != "constantes":
                            print("\t\tNivel C------> ", c, " : ", self.memoria[a][b][c])
                        else:
                            print("\t\tNivel C------> ", c)
                            for d in self.memoria[a][b][c]:
                                if d != "referencia_Globales":
                                    print("\t\t\tNivel D------> ", d, " : ", self.memoria[a][b][c][d])
                                else:
                                    print("\t\t\tNivel D------> ", d)
                                    for e in self.memoria[a][b][c][d]:
                                        if e != "variables" and e != "temporales" and e!= "constantes":
                                            print("\t\t\t\tNivel E------> ", e, " : ", self.memoria[a][b][c][d][e])
                                        else:
                                            print("\t\t\t\tNivel E------> ", e)
                                            for f in self.memoria[a][b][c][d][e]:
                                                print("\t\t\t\t\tNivel F------> ", f, " : ", self.memoria[a][b][c][d][e][f])
                                                
                    
            else:
                for b in self.memoria[a]:
                    if b != "variables" and b!= "temporales" and b!="constantes":
                        print("\tNivel B------> ", b, " : ", self.memoria[a][b])
                    else:
                        print("\tNivel B------> ", b)
                        for c in self.memoria[a][b]:
                            if c != "referencia_Globales":
                                print("\t\tNivel C------> ", c ," : ",self.memoria[a][b][c])
                            else:
                                print("\t\tNivel C------> ", c)
                                for d in self.memoria[a][b][c]:
                                    if d != "variables" and d != "temporales" and d!= "constantes":
                                        print("\t\t\tNivel D------> ", d, " : " ,self.memoria[a][b][c][d])
                                    else:
                                        print("\t\t\tNivel D------> ", d)
                                        for e in self.memoria[a][b][c][d]:
                                            print("\t\t\t\tNivel E------> ", e ," : ",self.memoria[a][b][c][d][e])
        

    def start(self):
        while self.indice < len(self.cuadruplos):
            
            #####################################################
            if self.cuadruplos[self.indice].get_operador() == "+":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']

                if self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['temporales'].keys():
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq + der
                else:
                    self.memoria[self.scopePrevio]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq + der


            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "-":
##                self.cuadruplos[self.indice].print_cuadruplo()
##                self.print_memoria()
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']

                if self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['temporales'].keys():
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq - der
                else:
                    self.memoria[self.scopePrevio]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq - der

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "*":
                
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']

                if self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['temporales'].keys():
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq * der
                else:
                    self.memoria[self.scopePrevio]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq * der

            #####################################################           
            elif self.cuadruplos[self.indice].get_operador() == "/":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']

                if self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['temporales'].keys():
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq / der
                else:
                    self.memoria[self.scopePrevio]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq / der

            #####################################################      
            elif self.cuadruplos[self.indice].get_operador() == ">":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']
                        
                if (izq > der):
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = True
                else:
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = False

            #####################################################                   
            elif self.cuadruplos[self.indice].get_operador() == "<":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']
                        
                if (izq < der):
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = True
                else:
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = False

            #####################################################               
            elif self.cuadruplos[self.indice].get_operador() == "<>":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']
                        
                if (izq != der):
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = True
                else:
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = False

            ##################################################### 
            elif self.cuadruplos[self.indice].get_operador() == "==":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria['globales']['variables'].keys():
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria[self.cuadruplos[self.indice].get_operando2()]['valor']
                        
                if (izq == der):
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = True
                else:
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = False

            ##################################################### 
            elif self.cuadruplos[self.indice].get_operador() == "=":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float or type(self.cuadruplos[self.indice].get_operando1()) == bool or (self.cuadruplos[self.indice].get_operando1()[:1]=='"' and self.cuadruplos[self.indice].get_operando1()[-1:]=='"')):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria[self.cuadruplos[self.indice].get_operando1()]['valor']

                if self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['variables'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq

                elif self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['temporales'].keys():
                    self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq

                else:
                    self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "goto":
                self.indice = self.cuadruplos[self.indice].get_resultado() - 1
                    
            #####################################################               
            elif self.cuadruplos[self.indice].get_operador() == "GotoF":
                if(type(self.cuadruplos[self.indice].get_operando1()) == bool):
                    resultado = bool(self.cuadruplos[self.indice].get_operando1())
                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        resultado = bool(self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"])

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        resultado = bool(self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"])

                    else:
                        resultado = bool(self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"])

                if resultado == False:
                    self.indice = self.cuadruplos[self.indice].get_resultado() - 1
                    
            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "retorno":
                self.cuadruplos[self.indice].print_cuadruplo()
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float or type(self.cuadruplos[self.indice].get_operando1()) == bool or (self.cuadruplos[self.indice].get_operando1()[:1]=='"' and self.cuadruplos[self.indice].get_operando1()[-1:]=='"')):
                    self.memoria[self.scope]['valor'] = self.cuadruplos[self.indice].get_operando1()
                    self.pila_de_valores_de_retorno.append(self.memoria[self.scope]['valor'])

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        self.memoria[self.scope]['valor'] = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]['valor']
                        self.pila_de_valores_de_retorno.append(self.memoria[self.scope]['valor'])

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        self.memoria[self.scope]['valor'] = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]['valor']
                        self.pila_de_valores_de_retorno.append(self.memoria[self.scope]['valor'])

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria['globales']['variables'].keys():
                        self.memoria[self.scope]['valor'] = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]['valor']
                        self.pila_de_valores_de_retorno.append(self.memoria[self.scope]['valor'])
                                                              

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "ret":
                self.cuadruplos[self.indice].print_cuadruplo()
                print("Pila de ejecucion antes del regreso: ", self.pila_de_ejecucion)
                input()
                retorno = self.pila_de_cuadruplo_de_retorno.pop()
                self.indice = retorno - 1
                self.contadorRecursividad -= 1
                
                if(len(self.pila_de_ejecucion) > 1):
                    actual = self.pila_de_ejecucion.pop()
                    procedimientoPendiente = self.pila_de_ejecucion.pop()
                    
                    if (procedimientoPendiente[:10] == "pendiente_"):
                        self.memoria[actual] = {}
                        self.memoria[actual] = dict(self.memoria[procedimientoPendiente])
                        self.scopePrevio = procedimientoPendiente
                        self.scope = actual
                        self.pila_de_ejecucion.append(actual)

                    else:
                        self.scopePrevio = self.scope
                        self.scope = procedimientoPendiente
                        self.pila_de_ejecucion.append(procedimientoPendiente)
                else:
                    self.scopePrevio = self.scope
                    actual = self.pila_de_ejecucion.pop()
                    self.scope = actual

                print("Pila de ejecucion despues del regreso: ", self.pila_de_ejecucion)
                input()

                        
                        
            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "era":
                if self.contadorInicial > 0:
                    actual = self.pila_de_ejecucion.pop()
                    self.memoria["pendiente_" + str(self.contadorRecursividad) + "_" + actual] = dict(self.memoria[actual])
                    self.pila_de_ejecucion.append("pendiente_" + str(self.contadorRecursividad) + "_" + actual)
                    self.scopePrevio = "pendiente_" + str(self.contadorRecursividad) + "_" + actual
                    self.contadorRecursividad += 1
                    self.memoria[actual] = dict(self.memoria['originales']["original_" + actual])
                    self.scope = self.cuadruplos[self.indice].get_operando1()
                    self.pila_de_ejecucion.append(self.cuadruplos[self.indice].get_operando1())

                else:
                    for a in self.memoria:
                        if a != 'globales' and a != 'main':
                            self.memoriaTemporal["original_" + a] = dict(self.memoria[a])
                    self.memoria['originales'] = dict(self.memoriaTemporal)
                    self.scopePrevio = self.scope
                    self.scope = self.cuadruplos[self.indice].get_operando1()
                    self.pila_de_ejecucion.append(self.cuadruplos[self.indice].get_operando1())
                    self.contadorInicial += 1

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "param":

                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float or type(self.cuadruplos[self.indice].get_operando1()) == bool or (self.cuadruplos[self.indice].get_operando1()[:1]=='"' and self.cuadruplos[self.indice].get_operando1()[-1:]=='"')):
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.cuadruplos[self.indice].get_operando1()
               
                if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scopePrevio]['variables'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria[self.scopePrevio]['variables'][self.cuadruplos[self.indice].get_operando1()]['valor']

                elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scopePrevio]['temporales'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria[self.scopePrevio]['temporales'][self.cuadruplos[self.indice].get_operando1()]['valor']

                elif self.cuadruplos[self.indice].get_operando1()  in self.memoria['globales']['variables'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]['valor']
    
                elif self.cuadruplos[self.indice].get_operando1() in self.memoria.keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria[self.scopePrevio]['valor']

                    
            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "gosub":
                self.pila_de_cuadruplo_de_retorno.append(self.indice + 1)
                self.indice = self.cuadruplos[self.indice].get_resultado() - 1
                
            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "print":
                if (type(self.cuadruplos[self.indice].get_resultado()) == int or type(self.cuadruplos[self.indice].get_resultado()) == float or type(self.cuadruplos[self.indice].get_resultado()) == bool or (self.cuadruplos[self.indice].get_resultado()[:1]=='"' and self.cuadruplos[self.indice].get_resultado()[-1:]=='"')):
                    if (self.cuadruplos[self.indice].get_resultado()[:1]=='"' and self.cuadruplos[self.indice].get_resultado()[-1:]=='"'):
                        print(self.cuadruplos[self.indice].get_resultado().strip('"'))
                    else:
                        print(self.cuadruplos[self.indice].get_resultado())

                else:
                    if self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['variables'].keys():
                        print(self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_resultado()]["valor"])

                    elif self.cuadruplos[self.indice].get_resultado() in self.memoria[self.scope]['temporales'].keys():
                        print(self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"])

                    else:
                        print(self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_resultado()]["valor"])
                
            self.indice += 1

            
            

    
