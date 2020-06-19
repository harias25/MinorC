#Clase principal para el manejo de los simbolos que soportará el programa

from enum import Enum
from ast.Expresion import Expresion

class TIPO_DATO(Enum) :
    ENTERO = 1,
    FLOAT = 2,
    CHAR = 3

class Simbolo(Expresion) :
    def __init__(self, id, temporal,tipo, linea,columna) :
        self.id = id
        self.temporal = temporal
        self.linea = linea
        self.columna = columna
        self.tipo = tipo


    def getTipo(self):
        
        return self.tipo

