from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D

class For(Instruccion) :
    def __init__(self, instruccion, condicion, operacion, instrucciones,linea,columna) :
        self.instruccion = instruccion
        self.operacion = operacion
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):

        tsFor = TS.Entorno(ent)
        instruccion3D = self.instruccion.traducir(tsFor,arbol,ventana)
        condicion3D = self.condicion.traducir(tsFor,arbol)
        if(condicion3D == None): return None
        etiquetaFor = temp.etiqueta()
        etiquetaSalida = temp.etiqueta()

        temp.listaContinue(0,etiquetaFor)
        temp.listaBreak(0,etiquetaSalida)

        ventana.consola.appendPlainText(etiquetaFor+":") 
        if(condicion3D.codigo3D!=""): ventana.consola.appendPlainText(condicion3D.codigo3D) 
        ventana.consola.appendPlainText("if(!"+condicion3D.temporal.utilizar()+") goto "+etiquetaSalida+";")
        for ins in self.instrucciones:
        #try:
            ins.traducir(tsFor,arbol,ventana)
        #except:
        #    pass

        self.operacion.traducir(tsFor,arbol,ventana)
        ventana.consola.appendPlainText("goto "+etiquetaFor+";") 
        ventana.consola.appendPlainText(etiquetaSalida+":") 

        temp.listaContinue(2,etiquetaFor)
        temp.listaBreak(2,etiquetaSalida)

       
        