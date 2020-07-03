from enum import Enum
from Optimizador.OptimizadorAST.Expresion import Expresion
from Optimizador.OptimizadorAST.Simbolo import TIPO_DATO as Tipo, Simbolo
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class TIPO_OPERACION(Enum) :
    SUMA = 1
    RESTA= 2
    MULTIPLICACION= 3
    DIVISION= 4
    MODULO= 5
    POTENCIA= 6
    MENOS_UNARIO= 7
    MAYOR_QUE= 8
    MENOR_QUE= 9
    MAYOR_IGUA_QUE= 10
    MENOR_IGUA_QUE= 11
    IGUAL_IGUAL= 12
    DIFERENTE_QUE= 13
    PRIMITIVO= 14
    OR= 15
    AND= 16
    NOT= 17
    TERNARIO= 18
    ID = 19
    XOR = 20
    ABSOLUTO = 21
    NOTR = 22
    PAND = 23
    BOR = 24
    XORR = 25
    SHIFTI = 26
    SHIFTD = 27
    ACCESO = 28

class Operacion(Expresion):
    def __init__(self):
        self.tipo           = None     #Tipo de Operacion
        self.ternario       = None     #Expresion Ternaria
        self.operadorIzq    = None     #Expresion
        self.operadorDer    = None     #Expresion
        self.valor          = None     #Object
        self.linea          = 0
        self.columna        = 0

    def Primitivo(self,valor):
        self.tipo = TIPO_OPERACION.PRIMITIVO
        self.valor = valor

    def Indentficador(self,valor,linea,columna):
        self.tipo = TIPO_OPERACION.ID 
        self.valor = valor

    def Operacion(self,izq,der,operacion,linea,columna):
        self.tipo = operacion
        self.operadorIzq = izq
        self.operadorDer = der
        self.linea = linea
        self.columna = columna 

    def OperacionUnaria(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.MENOS_UNARIO
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def ValorAbsoluto(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.ABSOLUTO
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def AccesoLista(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.ACCESO
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def OperacionNot(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.NOT
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def OperacionNotBit(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.NOTR
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna
    
    
    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado


    def generarAugus(self):
        #PRIMITIVOS
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.generarAugus()

        #ACCESOS LISTAS
        elif(self.tipo == TIPO_OPERACION.ACCESO):
            return self.operadorIzq.generarAugus()
            
        #IDENTIFICADORES
        elif(self.tipo == TIPO_OPERACION.ID):
            simbolo = Simbolo(self.valor,self.linea,self.columna)
            return simbolo.generarAugus()

        #SUMA
        elif(self.tipo == TIPO_OPERACION.SUMA):
            return self.operadorIzq.generarAugus() + "+" + self.operadorDer.generarAugus()

        #RESTA
        elif(self.tipo == TIPO_OPERACION.RESTA):
            return self.operadorIzq.generarAugus() + "-" + self.operadorDer.generarAugus()

        #MULTIPLICACIÓN
        elif(self.tipo == TIPO_OPERACION.MULTIPLICACION):
            return self.operadorIzq.generarAugus() + "*" + self.operadorDer.generarAugus()
            
        
        #DIVISION
        elif(self.tipo == TIPO_OPERACION.DIVISION):
            return self.operadorIzq.generarAugus() + "/" + self.operadorDer.generarAugus()
            
        #MODULO
        elif(self.tipo == TIPO_OPERACION.MODULO):
            return self.operadorIzq.generarAugus() + "%" + self.operadorDer.generarAugus()
            

        #UNARIA
        elif(self.tipo == TIPO_OPERACION.MENOS_UNARIO):
            return "-"+self.operadorIzq.generarAugus()

        #ABSOLUTO
        elif(self.tipo == TIPO_OPERACION.ABSOLUTO):
            return "abs("+self.operadorIzq.generarAugus()+")"
            
        
        #MAYOR
        elif(self.tipo == TIPO_OPERACION.MAYOR_QUE):
            return self.operadorIzq.generarAugus() + ">" + self.operadorDer.generarAugus()
            
        #MAYOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MAYOR_IGUA_QUE):
            return self.operadorIzq.generarAugus() + ">=" + self.operadorDer.generarAugus()
            
        #MENOR
        elif(self.tipo == TIPO_OPERACION.MENOR_QUE):
            return self.operadorIzq.generarAugus() + "<" + self.operadorDer.generarAugus()
            
        #MENOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MENOR_IGUA_QUE):
            return self.operadorIzq.generarAugus() + "<=" + self.operadorDer.generarAugus()
            
        #IGUAL
        elif(self.tipo == TIPO_OPERACION.IGUAL_IGUAL):
            return self.operadorIzq.generarAugus() + "==" + self.operadorDer.generarAugus()
            
        #DIFERENTE
        elif(self.tipo == TIPO_OPERACION.DIFERENTE_QUE):
            return self.operadorIzq.generarAugus() + "!=" + self.operadorDer.generarAugus()

        #AND
        elif(self.tipo == TIPO_OPERACION.AND):
            return self.operadorIzq.generarAugus() + "&&" + self.operadorDer.generarAugus()

        #OR
        elif(self.tipo == TIPO_OPERACION.OR):
            return self.operadorIzq.generarAugus() + "||" + self.operadorDer.generarAugus()

        #XOR
        elif(self.tipo == TIPO_OPERACION.XOR):
            return self.operadorIzq.generarAugus() + "xor" + self.operadorDer.generarAugus()
        #NOT
        elif(self.tipo == TIPO_OPERACION.NOT):
            return "!"+self.operadorIzq.generarAugus()
                
        #PAND
        elif(self.tipo == TIPO_OPERACION.PAND):
            return self.operadorIzq.generarAugus() + "&" + self.operadorDer.generarAugus()

        #BOR
        elif(self.tipo == TIPO_OPERACION.BOR):
            return self.operadorIzq.generarAugus() + "|" + self.operadorDer.generarAugus()

        #XORR
        elif(self.tipo == TIPO_OPERACION.XORR):
            return self.operadorIzq.generarAugus() + "^" + self.operadorDer.generarAugus()

        #SHIFI
        elif(self.tipo == TIPO_OPERACION.SHIFTI):
            return self.operadorIzq.generarAugus() + "<<" + self.operadorDer.generarAugus()

        #SHIFD
        elif(self.tipo == TIPO_OPERACION.SHIFTD):
            return self.operadorIzq.generarAugus() + ">>" + self.operadorDer.generarAugus()

        #NOTR
        elif(self.tipo == TIPO_OPERACION.NOTR):
            return "~"+self.operadorIzq.generarAugus()
        

    def invertirCondicion(self):
        #MAYOR
        #if(self.tipo == TIPO_OPERACION.MAYOR_QUE):
        #    return self.operadorIzq.generarAugus() + "<=" + self.operadorDer.generarAugus()
            
        #MAYOR IGUAL
        #elif(self.tipo == TIPO_OPERACION.MAYOR_IGUA_QUE):
        #    return self.operadorIzq.generarAugus() + "<" + self.operadorDer.generarAugus()
            
        #MENOR
        #elif(self.tipo == TIPO_OPERACION.MENOR_QUE):
        #    return self.operadorIzq.generarAugus() + ">=" + self.operadorDer.generarAugus()
            
        #MENOR IGUAL
        #elif(self.tipo == TIPO_OPERACION.MENOR_IGUA_QUE):
        #    return self.operadorIzq.generarAugus() + ">" + self.operadorDer.generarAugus()
            
        #IGUAL
        if(self.tipo == TIPO_OPERACION.IGUAL_IGUAL):
            return self.operadorIzq.generarAugus() + "!=" + self.operadorDer.generarAugus()
            
        #DIFERENTE
        elif(self.tipo == TIPO_OPERACION.DIFERENTE_QUE):
            return self.operadorIzq.generarAugus() + "==" + self.operadorDer.generarAugus()
        #NOT
        elif(self.tipo == TIPO_OPERACION.NOT):
            return self.operadorIzq.generarAugus()
        else:
            return self.generarAugus()


    def validarRegla1(self,varActual,varAsigna,varPrevia,varAsignaPrevia):
        if(varAsignaPrevia==varActual and varPrevia == varAsigna):
            return True
        return False

    def validarRegla4(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorIzq.generarAugus()
            value2 = self.operadorDer.generarAugus()
            if(value == value2):
                return True
        elif self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.ID:
            value = self.operadorIzq.generarAugus()
            value2 = self.operadorDer.generarAugus()
            if(value == value2):
                return True
        return False

    def validarRegla5(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorIzq.generarAugus()
            value2 = self.operadorDer.generarAugus()
            if(value != value2):
                return True
        return False

    # temporal = temporal + 0
    # temporal = 0 + temporal
    def validarRegla8(self,id):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            if(self.operadorIzq.valor == id):
                value = self.operadorDer.generarAugus()
                if(value == "0"):
                    return True
        
        elif self.operadorDer.tipo == TIPO_OPERACION.ID and self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO:
            if(self.operadorDer.valor == id):
                value = self.operadorIzq.generarAugus()
                if(value == "0"):
                    return True

        return False

    # temporal = temporal - 0
    def validarRegla9(self,id):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            if(self.operadorIzq.valor == id):
                value = self.operadorDer.generarAugus()
                if(value == "0"):
                    return True

        return False

    # temporal = temporal * 1
    # temporal = 1 * temporal
    def validarRegla10(self,id):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            if(self.operadorIzq.valor == id):
                value = self.operadorDer.generarAugus()
                if(value == "1"):
                    return True
        elif self.operadorDer.tipo == TIPO_OPERACION.ID and self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO:
            if(self.operadorDer.valor == id):
                value = self.operadorIzq.generarAugus()
                if(value == "1"):
                    return True

        return False

    # temporal = temporal / 1
    def validarRegla11(self,id):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            if(self.operadorIzq.valor == id):
                value = self.operadorDer.generarAugus()
                if(value == "1"):
                    return True

        return False

    # temporal = temporal2 + 0
    # temporal = 0 + temporal2
    def validarRegla12(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorDer.generarAugus()
            if(value == "0"):
                return self.operadorIzq.valor
        
        elif self.operadorDer.tipo == TIPO_OPERACION.ID and self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorIzq.generarAugus()
            if(value == "0"):
                return self.operadorDer.valor

        return ""

    # temporal = temporal2 - 0
    def validarRegla13(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorDer.generarAugus()
            if(value == "0"):
                return self.operadorIzq.valor

        return ""

    # temporal = tempora2 * 1
    # temporal = 1 * tempora2 
    def validarRegla14(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorDer.generarAugus()
            if(value == "1"):
                return self.operadorIzq.valor

        elif self.operadorDer.tipo == TIPO_OPERACION.ID and self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorIzq.generarAugus()
            if(value == "1"):
                return self.operadorDer.valor

        return ""

    # temporal = tempora2 / 1
    def validarRegla15(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorDer.generarAugus()
            if(value == "1"):
                return self.operadorIzq.valor

        return ""

    # temporal = temporal * 2
    def validarRegla16(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.ID and self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorDer.generarAugus()
            if(value == "2"):
                return self.operadorIzq.valor + " + " + self.operadorIzq.valor

        return ""

    # temporal = temporal * 0
    def validarRegla17(self):
        if self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorDer.generarAugus()
            if(value == "0"):
                return "0"

        elif self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO:
            value = self.operadorIzq.generarAugus()
            if(value == "0"):
                return "0"

        return ""

    # temporal = 0 / temporal
    def validarRegla18(self):
        if self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO and self.operadorDer.tipo == TIPO_OPERACION.ID :
            value = self.operadorIzq.generarAugus()
            if(value == "0"):
                return "0"

        return ""