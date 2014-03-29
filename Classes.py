class Cuadruplo: 
    def __init__(self):
        self.operador = ''
        self.operando1 = 0
        self.operando2 = 0
        self.resultado = ""

    def set_operador(self, operador): 
        self.operador = operador

    def set_operando1(self, operando1):
        self.operando1 = operando1

    def set_operando2(self, operando2):
        self.operando2 = operando2

    def set_resultado(self, resultado):
        self.resultado = resultado
    
    def get_operador(self): 
        return self.operador

    def get_operando1(self):
        return self.operando1

    def get_operando2(self):
        return self.operando2

    def get_resultado(self):
        return self.resultado

    
