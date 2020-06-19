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
                    if(self.tipo == "int"):
                        traduccion = temporal +"=0;"
                    elif(self.tipo == "float"):
                        traduccion = temporal +"=0.0;"
                    elif(self.tipo == "char"):
                        traduccion = temporal +"='';"   

                    ent.agregar(simbolo)
                    ventana.consola.appendPlainText(traduccion) 
                else:
                    traduccionExpresion = self.valor.traducir(ent,arbol)
                    if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D) 
                    traduccion = temporal + "="+traduccionExpresion.temporal.utilizar()+"; "
                    ent.agregar(simbolo)
                    ventana.consola.appendPlainText(traduccion) 
            
            contador = contador + 1