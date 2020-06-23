from ast.Instruccion import Instruccion
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.AccesoStruct import AccesoStruct 
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor

    def traducir(self,ent,arbol,ventana):


        traduccionExpresion = self.valor.traducir(ent,arbol)
        if(traduccionExpresion == None): return None

        #acceso a struct
        if(isinstance(self.id,AccesoStruct)):
            acceso = self.id.traducir(ent,arbol)
            if(acceso == None): return None

            if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D)
            ventana.consola.appendPlainText(acceso.codigo3D + "="+traduccionExpresion.temporal.utilizar()+"; ") 
            return None


        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, no se encuentra declarado un identificador con el nombre "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D)

            #casteos implicitos de C
        if(simbolo.tipo == Tipo.ENTERO):
            if(traduccionExpresion.tipo == Tipo.ENTERO):
                traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
            else:
                valor = traduccionExpresion.temporal.utilizar()
                if(traduccionExpresion.tipo == Tipo.FLOAT): #FLOAT A INT
                    if(str(valor).isnumeric()):
                        traduccion = simbolo.temporal + "="+ str(int(float(valor)))+"; "
                    else:
                        traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
                elif (traduccionExpresion.tipo == Tipo.CHAR): #CHAR A INT
                    if(len(str(valor))==1):
                        traduccion = simbolo.temporal + "="+str(int(valor))+"; "
                    else:
                        traduccion = simbolo.temporal + "="+valor+"; "
                else:
                    traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "  

        elif(simbolo.tipo == Tipo.FLOAT or simbolo.tipo == Tipo.DOOBLE):
            if(traduccionExpresion.tipo == Tipo.FLOAT):
                traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
            else:
                valor = traduccionExpresion.temporal.utilizar()
                if(traduccionExpresion.tipo == Tipo.ENTERO): #INT A FLOAT
                    if(str(valor).isnumeric()):
                        traduccion = simbolo.temporal + "="+str(float(int(valor)))+"; "
                    else:
                        traduccion = simbolo.temporal + "="+valor+"; "
                elif (traduccionExpresion.tipo == Tipo.CHAR): #CHAR A FLOAT
                    if(len(str(valor))==1):
                        traduccion = simbolo.temporal + "="+str(float(valor))+"; "
                    else:
                        traduccion = simbolo.temporal + "="+valor+"; "
                else:
                    traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "  

        elif(simbolo.tipo == Tipo.CHAR):
            if(traduccionExpresion.tipo == Tipo.CHAR):
                traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
            else:
                valor = traduccionExpresion.temporal.utilizar()
                if(traduccionExpresion.tipo == Tipo.ENTERO): #INT A CHAR
                    if(str(valor).isnumeric()):
                        if(isinstance(valor,float)):  
                            valor = int(float(valor))
                            if(isinstance(valor,int)):
                                valor = int(valor)
                                if(valor >255): 
                                    valor = valor - 256
                                value = chr(value)
                                
                                traduccion = simbolo.temporal + "="+value+"; "
                    else:
                        traduccion = simbolo.temporal + "="+valor+"; "
                elif (traduccionExpresion.tipo == Tipo.FLOAT): #FLOAT A CHAR
                    if(str(valor).isnumeric()):
                        if(isinstance(valor,float)):  
                            valor = int(float(valor))
                            if(isinstance(valor,int)):
                                valor = int(valor)
                                if(valor >255): 
                                    valor = valor - 256
                                value = chr(value)
                            traduccion = simbolo.temporal + "="+value+"; "
                        else:
                            traduccion = simbolo.temporal + "="+valor+"; "
                else:
                    traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "  

        else:
            traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "  

        ventana.consola.appendPlainText(traduccion) 