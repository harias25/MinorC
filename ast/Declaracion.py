from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from ast.Simbolo import Simbolo
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp


class Declaracion(Instruccion):

    def __init__(self,tipo,lista_id,valor,linea, columna):
        self.lista = lista_id
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo = tipo
    
    def traducir(self,ent,arbol,ventana):
        contador = 0
        for id in self.lista:
            #validar si existe el simbolo dentro de la tabla
            if(ent.existe(id)):
                error = Error("SEMANTICO","Error semantico, ya se encuentra declarado un identificador con el nombre "+id,self.linea,self.columna)
                ReporteErrores.func(error)
            else:
                traduccion = ""
                temporal = temp.temporal()
                simbolo = Simbolo(id,temporal,self.tipo,self.linea,self.columna)

                if(self.valor == None or (self.valor !=None and contador<(len(self.lista)-1))):
                    if(self.tipo == Tipo.ENTERO):
                        traduccion = temporal +"=0;"
                    elif(self.tipo == Tipo.FLOAT):
                        traduccion = temporal +"=0.0;"
                    elif(self.tipo == Tipo.CHAR):
                        traduccion = temporal +"='';"   

                    ent.agregar(simbolo)
                    ventana.consola.appendPlainText(traduccion) 
                else:
                    traduccionExpresion = self.valor.traducir(ent,arbol)
                    if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D) 


                    #casteos implicitos de C
                    if(self.tipo == Tipo.ENTERO):
                        if(traduccionExpresion.tipo == Tipo.ENTERO):
                            traduccion = temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
                        else:
                            valor = traduccionExpresion.temporal.utilizar()
                            if(traduccionExpresion.tipo == Tipo.FLOAT): #FLOAT A INT
                                if(str(valor).isnumeric):
                                    traduccion = temporal + "="+ str(int(float(valor)))+"; "
                                else:
                                    traduccion = temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
                            elif (traduccionExpresion.tipo == Tipo.CHAR): #CHAR A INT
                                if(len(str(valor))==1):
                                    traduccion = temporal + "="+str(int(valor))+"; "
                                else:
                                    traduccion = temporal + "="+valor+"; "

                    elif(self.tipo == Tipo.FLOAT):
                        if(traduccionExpresion.tipo == Tipo.FLOAT):
                            traduccion = temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
                        else:
                            valor = traduccionExpresion.temporal.utilizar()
                            if(traduccionExpresion.tipo == Tipo.INT): #INT A FLOAT
                                if(str(valor).isnumeric):
                                    traduccion = temporal + "="+str(float(int(valor)))+"; "
                                else:
                                    traduccion = temporal + "="+valor+"; "
                            elif (traduccionExpresion.tipo == Tipo.CHAR): #CHAR A FLOAT
                                if(len(str(valor))==1):
                                    traduccion = temporal + "="+str(float(valor))+"; "
                                else:
                                    traduccion = temporal + "="+valor+"; "

                    elif(self.tipo == Tipo.CHAR):
                        if(traduccionExpresion.tipo == Tipo.CHAR):
                            traduccion = temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
                        else:
                            valor = traduccionExpresion.temporal.utilizar()
                            if(traduccionExpresion.tipo == Tipo.INT): #INT A CHAR
                                if(str(valor).isnumeric):
                                    if(isinstance(valor,float)):  valor = int(float(valor))
                                    if(isinstance(valor,int)):
                                        valor = int(valor)
                                        if(valor >255): valor = valor - 256
                                        value = chr(value)
                                    traduccion = temporal + "="+value+"; "
                                else:
                                    traduccion = temporal + "="+valor+"; "
                            elif (traduccionExpresion.tipo == Tipo.FLOAT): #FLOAT A CHAR
                                if(str(valor).isnumeric):
                                    if(isinstance(valor,float)):  valor = int(float(valor))
                                    if(isinstance(valor,int)):
                                        valor = int(valor)
                                        if(valor >255): valor = valor - 256
                                        value = chr(value)
                                    traduccion = temporal + "="+value+"; "
                                else:
                                    traduccion = temporal + "="+valor+"; "

                    ent.agregar(simbolo)
                    ventana.consola.appendPlainText(traduccion) 
            
            contador = contador + 1