from ast.Instruccion import Instruccion
import ast.Temporales as temp

class Continue(Instruccion) :
    def __init__(self,linea,columna) :
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        ventana.editor.append("\n"+"goto "+temp.listaContinue(1,None)+";") 