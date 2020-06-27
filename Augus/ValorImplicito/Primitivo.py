from Augus.ast.Expresion import Expresion
from Augus.ast.Simbolo import TIPO_DATO as Tipo

class Primitivo(Expresion):
    def __init__(self,valor,linea,columna):
        self.valor          = valor     #Object
    
    def getValorImplicito(self,ent,arbol):
        return self.valor
    
