from ast.Instruccion import Instruccion
import ast.Temporales as temp

class Return(Instruccion) :
    def __init__(self,expresion,linea,columna) :
        self.linea = linea
        self.columna = columna
        self.expresion = expresion

    def traducir(self,ent,arbol,ventana):
        traduccionExpresion = self.expresion.traducir(ent,arbol,ventana)
        if(traduccionExpresion == None): return None

        if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D)
        ventana.consola.appendPlainText("$v0="+str(traduccionExpresion.temporal.utilizar())+";")
        etiqueta = temp.listaReturn(1,None)
        if(etiqueta!=None):
            ventana.consola.appendPlainText("goto "+etiqueta+";") 
            #temp.listaReturn(2,etiqueta)