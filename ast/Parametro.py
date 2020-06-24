from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
from ast.Simbolo import Simbolo
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ValorImplicito.Asignacion import Asignacion

class Parametro(Instruccion):

    def __init__(self,tipo,id,linea, columna):
        self.id = id
        self.linea = linea
        self.columna = columna
        self.tipo = tipo
        self.valor = None
        self.temporal = None

    def traducir(self,ent,arbol,ventana):
        if(ent.existe(self.id)):
            error = Error("SEMANTICO","Error semantico, ya se encuentra definido un parametro con el nombre "+id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        else:
            if(self.valor == None): 
                temporal = temp.parametro()
                simbolo = Simbolo(self.id,temporal,self.tipo,self.linea,self.columna)
                ent.agregar(simbolo)
                return temporal
            else:
                simbolo = Simbolo(self.id,self.temporal,self.tipo,self.linea,self.columna)
                ent.agregar(simbolo)
                asignacion = Asignacion(self.id,self.valor,self.linea,self.columna)
                asignacion.traducir(ent,arbol,ventana)