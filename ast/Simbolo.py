#Clase principal para el manejo de los simbolos que soportará el programa

from enum import Enum
from ast.Expresion import Expresion
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D


class TIPO_DATO(Enum) :
    ENTERO  = 1,
    FLOAT   = 2,
    CHAR    = 3,
    VOID    = 4,
    DOOBLE  = 5

class Simbolo(Expresion) :
    def __init__(self, id, temporal,tipo, linea,columna) :
        self.id = id
        self.temporal = temporal
        self.linea = linea
        self.columna = columna
        self.tipo = tipo
        self.llaves = None

    def traducir(self,ent,arbol):
        resultado3D = Resultado3D()
        resultado3D.codigo3D = ""
        resultado3D.tipo = self.tipo
        resultado3D.temporal = Temporal(str(self.temporal))
        return resultado3D
    
    def getTipo(self):
        
        return self.tipo.name

    def getTipoVar(self):
        if(self.llaves != None): return "ARRAY"

        return "IDENTIFICADOR"

