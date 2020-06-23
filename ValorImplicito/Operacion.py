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
    
    def traducir(self,ent,arbol):
        #PRIMITIVOS
        if(self.tipo == TIPO_OPERACION.PRIMITIVO):
            return self.valor.traducir(ent,arbol)

        #ACCESOS LISTAS
        elif(self.tipo == TIPO_OPERACION.ACCESO):
            return self.operadorIzq.getValorImplicito(ent,arbol)

        elif(self.tipo == TIPO_OPERACION.ACCESO_STRUCT):
            valor = self.operadorIzq.traducir(ent,arbol)
            if(valor == None ): return None
            valor.codigo3D = valor.temporal.utilizar() + "="+ valor.codigo3D + ";"
            return valor

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

            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"+"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  

            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #RESTA
        elif(self.tipo == TIPO_OPERACION.RESTA):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"-"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #MULTIPLICACIÓN
        elif(self.tipo == TIPO_OPERACION.MULTIPLICACION):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"*"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        
        #DIVISION
        elif(self.tipo == TIPO_OPERACION.DIVISION):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"/"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #MODULO
        elif(self.tipo == TIPO_OPERACION.MODULO):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"%"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #UNARIA
        elif(self.tipo == TIPO_OPERACION.MENOS_UNARIO):
            valor1 = self.operadorIzq.traducir(ent,arbol)
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
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+">"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        
        #MAYOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MAYOR_IGUA_QUE):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+">="+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        #MENOR
        elif(self.tipo == TIPO_OPERACION.MENOR_QUE):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"<"+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        
        #MENOR IGUAL
        elif(self.tipo == TIPO_OPERACION.MENOR_IGUA_QUE):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"<="+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #IGUAL
        elif(self.tipo == TIPO_OPERACION.IGUAL_IGUAL):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"=="+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result
        
        #DIFERENTE
        elif(self.tipo == TIPO_OPERACION.DIFERENTE_QUE):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+"!="+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #AND
        elif(self.tipo == TIPO_OPERACION.AND):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" && "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #OR
        elif(self.tipo == TIPO_OPERACION.OR):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" or "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #XOR
        elif(self.tipo == TIPO_OPERACION.XOR):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" xor "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #NOT
        elif(self.tipo == TIPO_OPERACION.NOT):
            valor1 = self.operadorIzq.traducir(ent,arbol)
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
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" & "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #BOR
        elif(self.tipo == TIPO_OPERACION.BOR):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" | "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #XORR
        elif(self.tipo == TIPO_OPERACION.XORR):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" ^ "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #SHIFI
        elif(self.tipo == TIPO_OPERACION.SHIFTI):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" << "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #SHIFD
        elif(self.tipo == TIPO_OPERACION.SHIFTD):
            valor1 = self.operadorIzq.traducir(ent,arbol)
            valor2 = self.operadorDer.traducir(ent,arbol)
            if(valor1 == None or valor2 == None): return None

            temporal = Temp.nuevoTemporal()
            op = temporal.obtener() + '='+valor1.temporal.utilizar()+" >> "+valor2.temporal.utilizar()+";"


            resultado = valor1.codigo3D
            if(resultado !="" and valor2.codigo3D):
                resultado = resultado + "\n" + valor2.codigo3D 
            else:
                resultado +=  valor2.codigo3D 

            if(resultado!=""):
                resultado = resultado + "\n" + op
            else:
               resultado +=  op  
               
            result = Resultado3D()
            result.codigo3D = resultado
            result.temporal = temporal
            result.tipo = Tipo.FLOAT
            return result

        #NOTR
        elif(self.tipo == TIPO_OPERACION.NOTR):
            valor1 = self.operadorIzq.traducir(ent,arbol)
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
        

    