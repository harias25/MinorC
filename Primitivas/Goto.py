from ast.Instruccion import Instruccion

class Goto(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        ventana.editor.append("\n"+"goto "+self.id+";") 