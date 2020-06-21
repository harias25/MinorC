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
    
    def traducir(self,ent,arbol,ventana):
        if(ent.existe(self.id)):
            error = Error("SEMANTICO","Error semantico, ya se encuentra definido un parametro con el nombre "+id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        else:
            temporal = temp.parametro()
            simbolo = Simbolo(id,temporal,self.tipo,self.linea,self.columna)
            ent.agregar(simbolo)
            return temporal