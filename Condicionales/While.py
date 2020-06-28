from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D
from Transferencia.Break import Break
from Transferencia.Continue import Continue

class While(Instruccion) :
    def __init__(self, condicion, instrucciones,linea,columna) :
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        condicion3D = self.condicion.traducir(ent,arbol,ventana)
        if(condicion3D == None): return None
        etiquetaWhile = temp.etiqueta()
        etiquetaSalida = temp.etiqueta()

        temp.listaContinue(0,etiquetaWhile)
        temp.listaBreak(0,etiquetaSalida)

        ventana.editor.append("\n"+etiquetaWhile+":") 
        if(condicion3D.codigo3D!=""): ventana.editor.append("\n"+condicion3D.codigo3D) 
        ventana.editor.append("\n"+"if(!"+condicion3D.temporal.utilizar()+") goto "+etiquetaSalida+";")

        tsWhile = TS.Entorno(ent)
        for ins in self.instrucciones:
            try:
                ins.traducir(tsWhile,arbol,ventana)
            except:
                pass
        
        ventana.editor.append("\n"+"goto "+etiquetaWhile+";")

        ventana.editor.append("\n"+etiquetaSalida+":")

        temp.listaContinue(2,etiquetaWhile)
        temp.listaBreak(2,etiquetaSalida)
        
        

