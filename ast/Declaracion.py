from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from ast.Simbolo import Simbolo
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ValorImplicito.Asignacion import Asignacion

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
                return None
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
                    else:
                        struct = arbol.obtenerStruct(self.tipo)
                        if(struct == None):
                            error = Error("SEMANTICO","Error semantico, no se encuentra declarado un struct con el nombre "+self.tipo,self.linea,self.columna)
                            ReporteErrores.func(error)
                            return None

                        traduccion = temporal +"=array();"

                    ent.agregar(simbolo)
                    ventana.editor.append("\n"+traduccion) 
                else:
                    ent.agregar(simbolo)
                    asignacion = Asignacion(id,self.valor,self.linea,self.columna)
                    asignacion.traducir(ent,arbol,ventana)
            contador = contador + 1