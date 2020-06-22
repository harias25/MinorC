from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D

class DoWhile(Instruccion) :
    def __init__(self, condicion, instrucciones,linea,columna) :
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        condicion3D = self.condicion.traducir(ent,arbol)
        if(condicion3D == None): return None
        etiquetaWhile = temp.etiqueta()
        etiquetaSalida = temp.etiqueta()


        ventana.consola.appendPlainText(etiquetaWhile+":") 
        tsWhile = TS.Entorno(ent)
        for ins in self.instrucciones:
        #try:
            ins.traducir(tsWhile,arbol,ventana)
        #except:
        #    pass

        if(condicion3D.codigo3D!=""): ventana.consola.appendPlainText(condicion3D.codigo3D) 
        ventana.consola.appendPlainText("if("+condicion3D.temporal.utilizar()+") goto "+etiquetaWhile+";")

        
        

        
        

