from enum import Enum
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as Temp

from ast.Temporales import Temporal
from ast.Temporales import Resultado3D

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
    ACCESO_STRUCT = 29
    LLAMADA = 30

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

    def AccesoStruct(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.ACCESO_STRUCT
        self.operadorIzq = exp
        self.linea = linea
        self.columna = columna

    def Llamada(self,exp,linea,columna):
        self.tipo = TIPO_OPERACION.LLAMADA
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
    

    def validarLados(self,recursivo):
        if ((self.operadorIzq.tipo == TIPO_OPERACION.ID or self.operadorIzq.tipo == TIPO_OPERACION.PRIMITIVO) and (self.operadorDer.tipo == TIPO_OPERACION.ID or self.operadorDer.tipo == TIPO_OPERACION.PRIMITIVO)) and recursivo == 0:
            return True

        return False
    

    def generarOperacionBinaria(self,signo,ent,arbol,ventana,recursivo):
        valor1 = self.operadorIzq.traducir(ent,arbol,ventana,recursivo+1)
        valor2 = self.operadorDer.traducir(ent,arbol,ventana,recursivo+1)
        if(valor1 == None or valor2 == None): return None

        resultado = valor1.codigo3D
        if(resultado !="" and valor2.codigo3D):
            resultado = resultado + "\n" + valor2.codigo3D 
        else:
            resultado +=  valor2.codigo3D 

        if(resultado!=""):
            resultado = resultado + "\n" 

        result = Resultado3D()
        result.tipo = Tipo.FLOAT
        if(self.validarLados(recursivo)):
            temporal = Temp.Temporal(valor1.temporal.utilizar()+" "+signo+" "+valor2.temporal.utilizar())
            result.codigo3D = resultado
            result.temporal = temporal
            return result

        temporal = Temp.nuevoTemporal()
        op = temporal.obtener() + '='+valor1.temporal.utilizar()+" "+signo+" "+valor2.temporal.utilizar()+";"
        resultado +=  op  
        result.codigo3D = resultado
        result.temporal = temporal
        return result

    def traducir(self,ent,arbol,ventana,recursivo=0):
        #PRIMITIVOS
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.traducir(ent,arbol)

        #ACCESOS LISTAS
        elif(self.tipo == TIPO_OPERACION.ACCESO):
            valor = self.operadorIzq.traducir(ent,arbol,ventana)
            if(valor == None ): return None
            return valor

        elif(self.tipo == TIPO_OPERACION.ACCESO_STRUCT):
            valor = self.operadorIzq.traducir(ent,arbol,ventana)
            if(valor == None ): return None
            valor.codigo3D = valor.temporal.utilizar() + "="+ valor.codigo3D + ";"
            return valor

        elif(self.tipo == TIPO_OPERACION.LLAMADA):
            
            #etiquetaSalida = Temp.etiqueta()
            #Temp.listaReturn(0,etiquetaSalida)
            self.operadorIzq.traducir(ent,arbol,ventana)
            #ventana.editor.append("\n"+etiquetaSalida+":")
            result = Resultado3D()
            result.codigo3D = ""
            result.temporal = Temp.Temporal("$v0")
            result.tipo = Tipo.FLOAT
            return result

        #IDENTIFICADORES
        elif(self.tipo == TIPO_OPERACION.ID):
            simbolo = ent.obtener(str(self.valor))
            if(simbolo == None):
                error = Error("SEMANTICO","Error semantico, No es existe la variable "+str(self.valor),self.linea,self.columna)
                ReporteErrores.func(error)
                return None
            
            return simbolo.traducir(ent,arbol)

        #SUMA
        elif(self.tipo == TIPO_OPERACION.SUMA):
            return self.generarOperacionBinaria("+",ent,arbol,ventana,recursivo)
            
        #RESTA
        elif(self.tipo == TIPO_OPERACION.RESTA):
            return self.generarOperacionBinaria("-",ent,arbol,ventana,recursivo)

        #MULTIPLICACIÓN
        elif(self.tipo == TIPO_OPERACION.MULTIPLICACION):
            return self.generarOperacionBinaria("*",ent,arbol,ventana,recursivo)
        
        #DIVISION
        elif(self.tipo == TIPO_OPERACION.DIVISION):
            return self.generarOperacionBinaria("/",ent,arbol,ventana,recursivo)

        #MODULO
        elif(self.tipo == TIPO_OPERACION.MODULO):
            return self.generarOperacionBinaria("%",ent,arbol,ventana,recursivo)

        #UNARIA
        elif(self.tipo == TIPO_OPERACION.MENOS_UNARIO):
            valor1 = self.operadorIzq.traducir(ent,arbol,ventana,recursivo+1)
            if(valor1 == None): return None
            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '=-'+valor1.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        
        
        #MAYOR
        elif(self.tipo == TIPO_OPERACION.MAYOR_QUE):
            return self.generarOperacionBinaria(">",ent,arbol,ventana,recursivo)
        
        #MAYOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MAYOR_IGUA_QUE):
            return self.generarOperacionBinaria(">=",ent,arbol,ventana,recursivo)
        #MENOR
        elif(self.tipo == TIPO_OPERACION.MENOR_QUE):
            return self.generarOperacionBinaria("<",ent,arbol,ventana,recursivo)
        
        #MENOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MENOR_IGUA_QUE):
            return self.generarOperacionBinaria("<=",ent,arbol,ventana,recursivo)

        #IGUAL
        elif(self.tipo == TIPO_OPERACION.IGUAL_IGUAL):
            return self.generarOperacionBinaria("==",ent,arbol,ventana,recursivo)
        
        #DIFERENTE
        elif(self.tipo == TIPO_OPERACION.DIFERENTE_QUE):
            return self.generarOperacionBinaria("!=",ent,arbol,ventana,recursivo)

        #AND
        elif(self.tipo == TIPO_OPERACION.AND):
            return self.generarOperacionBinaria("&&",ent,arbol,ventana,recursivo)

        #OR
        elif(self.tipo == TIPO_OPERACION.OR):
            return self.generarOperacionBinaria("||",ent,arbol,ventana,recursivo)
        #XOR
        elif(self.tipo == TIPO_OPERACION.XOR):
            return self.generarOperacionBinaria("xor",ent,arbol,ventana,recursivo)

        #NOT
        elif(self.tipo == TIPO_OPERACION.NOT):
            valor1 = self.operadorIzq.traducir(ent,arbol,ventana,recursivo+1)
            if(valor1 == None): return None
            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '=!'+valor1.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
                
        #PAND
        elif(self.tipo == TIPO_OPERACION.PAND):
            return self.generarOperacionBinaria("&",ent,arbol,ventana,recursivo)

        #BOR
        elif(self.tipo == TIPO_OPERACION.BOR):
            return self.generarOperacionBinaria("|",ent,arbol,ventana,recursivo)

        #XORR
        elif(self.tipo == TIPO_OPERACION.XORR):
            return self.generarOperacionBinaria("^",ent,arbol,ventana,recursivo)
            

        #SHIFI
        elif(self.tipo == TIPO_OPERACION.SHIFTI):
            return self.generarOperacionBinaria("<<",ent,arbol,ventana,recursivo)

        #SHIFD
        elif(self.tipo == TIPO_OPERACION.SHIFTD):
            return self.generarOperacionBinaria(">>",ent,arbol,ventana,recursivo)
            
        #NOTR
        elif(self.tipo == TIPO_OPERACION.NOTR):
            valor1 = self.operadorIzq.traducir(ent,arbol,ventana,recursivo+1)
            if(valor1 == None): return None
            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '=~'+valor1.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        

    