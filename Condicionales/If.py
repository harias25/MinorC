from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D

class If(Instruccion) :
    def __init__(self, condicion, instruccionesV,instruccionesF,listaElseIF,linea,columna) :
        self.condicion = condicion
        self.instruccionesV = instruccionesV
        self.instruccionesF = instruccionesF
        self.listaElseIF = listaElseIF
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):

        tsIf = TS.Entorno(ent)
        resultCondition = self.condicion.traducir(tsIf,arbol,ventana)
        if(resultCondition == None): return None

        etiquetaTrue = temp.etiqueta()
        etiquetaFalse = temp.etiqueta()
        etiquetaSalida = temp.etiqueta()

        if(resultCondition.codigo3D!=""): ventana.editor.append("\n"+resultCondition.codigo3D) 
        
        ventana.editor.append("\n"+"if("+resultCondition.temporal.utilizar()+") goto "+etiquetaTrue+";")
        

        
        listaElseIf = []
        #SE CARGAN LAS ETIQUETAS DEL ELSE IF Y SE IMPRIMEN LAS CONDICIONES
        for ins in self.listaElseIF:
            etiquetaTrueElseIf = temp.etiqueta()
            resultConditionElseIf = ins.condicion.traducir(tsIf,arbol,ventana)
            if(resultConditionElseIf.codigo3D!=""): ventana.editor.append("\n"+resultConditionElseIf.codigo3D) 
            ventana.editor.append("\n"+"if("+resultConditionElseIf.temporal.utilizar()+") goto "+etiquetaTrueElseIf+";")
            listaElseIf.append(etiquetaTrueElseIf)

        if(len(self.instruccionesF)==0 and  len(self.listaElseIF) == 0):
            ventana.editor.append("\n"+"goto "+etiquetaSalida+";")

        if(len(self.instruccionesF)>0 and len(self.listaElseIF) == 0):
            ventana.editor.append("\n"+"goto "+etiquetaFalse+";")

        if(len(self.listaElseIF) > 0):
            ventana.editor.append("\n"+"goto "+etiquetaFalse+";")

        ventana.editor.append("\n"+etiquetaTrue+":")
        for ins in self.instruccionesV:
            try:
                ins.traducir(tsIf,arbol,ventana)
            except:
                pass
        ventana.editor.append("\n"+"goto "+etiquetaSalida+";")

        

        contador = 0
        for ins in self.listaElseIF:
            tsElseIf = TS.Entorno(ent)
            ventana.editor.append("\n"+listaElseIf[contador]+":")
            for inss in ins.instruccionesV:
                try:
                    inss.traducir(tsElseIf,arbol,ventana)
                except:
                    pass
            ventana.editor.append("\n"+"goto "+etiquetaSalida+";")
            contador = contador + 1
            arbol.entornoGlobal.tabla = {**tsElseIf.tabla,**arbol.entornoGlobal.tabla}
            
        if(len(self.instruccionesF)>0 and len(self.listaElseIF) > 0):
            ventana.editor.append("\n"+"goto "+etiquetaFalse+";")

        if(len(self.instruccionesF)>0):
            ventana.editor.append("\n"+etiquetaFalse+":")
            tsElse = TS.Entorno(ent)
            for ins in self.instruccionesF:
                try:
                    ins.traducir(tsElse,arbol,ventana)
                except:
                    pass
            arbol.entornoGlobal.tabla = {**tsElse.tabla,**arbol.entornoGlobal.tabla}

        ventana.editor.append("\n"+etiquetaSalida+":")
        arbol.entornoGlobal.tabla = {**tsIf.tabla,**arbol.entornoGlobal.tabla}