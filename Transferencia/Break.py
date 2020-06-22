from ast.Instruccion import Instruccion

class Break(Instruccion) :
    def __init__(self,linea,columna) :
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        pass