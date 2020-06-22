from ast.Instruccion import Instruccion

class Case(Instruccion) :
    def __init__(self, condicion,instrucciones,linea,columna) :
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        pass
        