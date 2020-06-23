from ast.Instruccion import Instruccion
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D

class Struct(Instruccion) :
    def __init__(self, id, declaraciones, linea,columna) :
        self.id = id
        self.declaraciones = declaraciones
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol):
       pass
    