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
        condicion3D = self.condicion.traducir(tsFor,arbol,ventana)
        if(condicion3D == None): return None
        etiquetaFor = temp.etiqueta()
        etiquetaSalida = temp.etiqueta()
        etiquetaVerdadero = temp.etiqueta()

        temp.listaContinue(0,etiquetaFor)
        temp.listaBreak(0,etiquetaSalida)

        ventana.editor.append("\n"+etiquetaFor+":") 
        if(condicion3D.codigo3D!=""): ventana.editor.append("\n"+condicion3D.codigo3D) 
        ventana.editor.append("\n"+"if("+condicion3D.temporal.utilizar()+") goto "+etiquetaVerdadero+";")
        ventana.editor.append("\n"+"goto "+etiquetaSalida+";") 

        ventana.editor.append("\n"+etiquetaVerdadero+":") 
        for ins in self.instrucciones:
            try:
                ins.traducir(tsFor,arbol,ventana)
            except:
                pass

        self.operacion.traducir(tsFor,arbol,ventana)
        ventana.editor.append("\n"+"goto "+etiquetaFor+";") 
        ventana.editor.append("\n"+etiquetaSalida+":") 

        temp.listaContinue(2,etiquetaFor)
        temp.listaBreak(2,etiquetaSalida)

       
        