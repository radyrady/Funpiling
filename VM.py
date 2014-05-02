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

    def get_cuadruplos(self):
        return cuadruplos

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

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq + der


            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "-":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq - der

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "*":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq * der

            #####################################################           
            elif self.cuadruplos[self.indice].get_operador() == "/":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_resultado()]["valor"] = izq / der

            #####################################################      
            elif self.cuadruplos[self.indice].get_operador() == ">":
                if (type(self.cuadruplos[self.indice].get_operando1()) == int or type(self.cuadruplos[self.indice].get_operando1()) == float):
                    izq = self.cuadruplos[self.indice].get_operando1()

                else:
                    if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['variables'].keys():
                        izq = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scope]['temporales'].keys():
                        izq = self.memoria[self.scope]['temporales'][self.cuadruplos[self.indice].get_operando1()]["valor"]

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]
                        
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

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]
                        
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

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]
                        
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

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]
                        
                if (type(self.cuadruplos[self.indice].get_operando2()) == int or type(self.cuadruplos[self.indice].get_operando2()) == float):
                    der = self.cuadruplos[self.indice].get_operando2()

                else:
                    if self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['variables'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    elif self.cuadruplos[self.indice].get_operando2() in self.memoria[self.scope]['temporales'].keys():
                        der = self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]

                    else:
                        der = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando2()]["valor"]
                        
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

                    else:
                        izq = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]["valor"]

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
                print("retorno")

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "ret":
                self.indice = self.indice_pasado - 1
                self.indice_pasado = self.indice + 1

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "era":
                self.scopePrevio = self.scope
                self.scope = self.cuadruplos[self.indice].get_operando1()
                self.pila_de_ejecucion.append(self.cuadruplos[self.indice].get_operando1())
                

            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "param":

                if self.cuadruplos[self.indice].get_operando1() in self.memoria[self.scopePrevio]['variables'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria[self.scopePrevio]['variables'][self.cuadruplos[self.indice].get_operando1()]['valor']

                if self.cuadruplos[self.indice].get_operando1()  in self.memoria[self.scopePrevio]['temporales'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria[self.scopePrevio]['temporales'][self.cuadruplos[self.indice].get_operando1()]['valor']

                if self.cuadruplos[self.indice].get_operando1()  in self.memoria['globales']['variables'].keys():
                    self.memoria[self.scope]['variables'][self.cuadruplos[self.indice].get_operando2()]['valor'] = self.memoria['globales']['variables'][self.cuadruplos[self.indice].get_operando1()]['valor']
                    
            #####################################################
            elif self.cuadruplos[self.indice].get_operador() == "gosub":
                self.indice_pasado = self.indice + 1
                print("Indice al que regresa: ", self.indice_pasado)
                self.indice = self.cuadruplos[self.indice].get_resultado() - 1
                print("Indice al que ira: ", self.indice + 1)
                
            
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

            
            

    
