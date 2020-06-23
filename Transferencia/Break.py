from ast.Instruccion import Instruccion
import ast.Temporales as temp

class Break(Instruccion) :
    def __init__(self,linea,columna) :
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        ventana.consola.appendPlainText("goto "+temp.listaBreak(1,None)+";") 