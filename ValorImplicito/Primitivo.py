from ast.Expresion import Expresion
from ast.Simbolo import TIPO_DATO as Tipo
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D



class Primitivo(Expresion):
    def __init__(self,valor,linea,columna):
        self.valor          = valor     #Object

    def traducir(self,ent,arbol):
        resultado3D = Resultado3D()
        resultado3D.codigo3D = ""


        if isinstance(self.valor, str):
            resultado3D.tipo = Tipo.CHAR
        elif isinstance(self.valor, int):
            resultado3D.tipo = Tipo.ENTERO
        elif isinstance(self.valor, float):
            resultado3D.tipo = Tipo.FLOAT

        if(resultado3D.tipo == Tipo.CHAR):
            resultado3D.temporal = Temporal("\""+self.valor+"\"")
        else:
            resultado3D.temporal = Temporal(str(self.valor))

        return resultado3D
    
