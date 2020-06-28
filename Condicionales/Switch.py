from ast.Instruccion import Instruccion
import ast.Entorno as TS
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D

class Switch(Instruccion) :
    def __init__(self, condicion, lista_case,default,linea,columna) :
        self.condicion = condicion
        self.lista_case = lista_case
        self.default = default
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        condicion3D = self.condicion.traducir(ent,arbol,ventana)
        if(condicion3D == None): return None
        if(condicion3D.codigo3D!=""): ventana.editor.append("\n"+condicion3D.codigo3D) 
        etiquetaSalida = temp.etiqueta()
        etiquetaDefault = temp.etiqueta()
        temp.listaBreak(0,etiquetaSalida)

        listaElseIf = []
        #SE CARGAN LAS ETIQUETAS DE LOS CASE Y SE IMPRIMEN LAS CONDICIONES
        for ins in self.lista_case:
            etiquetaTrueElseIf = temp.etiqueta()
            resultConditionElseIf = ins.condicion.traducir(ent,arbol,ventana)
            if(resultConditionElseIf == None): return None
            if(resultConditionElseIf.codigo3D!=""): ventana.editor.append("\n"+resultConditionElseIf.codigo3D) 
            ventana.editor.append("\n"+"if("+condicion3D.temporal.utilizar()+"=="+resultConditionElseIf.temporal.utilizar()+") goto "+etiquetaTrueElseIf+";")
            listaElseIf.append(etiquetaTrueElseIf)


        if(self.default!=None):
            ventana.editor.append("\n"+"goto "+etiquetaDefault+";")
        else:
            ventana.editor.append("\n"+"goto "+etiquetaSalida+";")


        contador = 0
        for ins in self.lista_case:
            tsElseIf = TS.Entorno(ent)
            ventana.editor.append("\n"+listaElseIf[contador]+":")
            for inss in ins.instrucciones:
                try:
                    inss.traducir(tsElseIf,arbol,ventana)
                except:
                    pass
            #ventana.editor.append("\n"+"goto "+etiquetaSalida+";")
            contador = contador + 1


        if(self.default!=None):
            ventana.editor.append("\n"+etiquetaDefault+":")
            entDefault = TS.Entorno(ent)
            for ins in self.default.instrucciones:
                try:
                    ins.traducir(entDefault,arbol,ventana)
                except:
                    pass

        ventana.editor.append("\n"+etiquetaSalida+":")
        temp.listaBreak(2,etiquetaSalida)