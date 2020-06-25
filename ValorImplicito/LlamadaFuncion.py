from ast.Instruccion import Instruccion
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.AccesoStruct import AccesoStruct 
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Entorno as TS
import ast.Temporales as temp


class LlamadaFuncion(Instruccion):
    def __init__(self,id,expresiones,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.expresiones = expresiones

    def traducir(self,ent,arbol,ventana):
        funcion = arbol.obtenerEtiqueta(self.id)
        if(funcion == None):
            error = Error("SEMANTICO","Error semantico, no se encuentra definida una Función con el nombre "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        if(len(funcion.parametros) != len(funcion.temporales)):
            error = Error("SEMANTICO","Error semantico, no se encuentra definida una Función con el nombre "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        if(len(funcion.parametros) != len(self.expresiones)):
            error = Error("SEMANTICO","Error semantico, El número de parametros no son iguales a los definidos en la función "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

       
        enLlamada = TS.Entorno(ent)
        contador = 0

        


        for parametro in funcion.parametros:
            parametro.valor = self.expresiones[contador]
            parametro.temporal = funcion.temporales[contador]
            parametro.traducir(enLlamada,arbol,ventana)
            contador = contador + 1

       

        
        
        llamadaAnterior = temp.listaLLamada(1,None)
        recursionAnterior = temp.listaRecusion(1,None)
        
        if(not recursionAnterior==self.id):
            etiquetaFuncion = temp.etiqueta()
            etiquetaSalida = temp.etiqueta()
            temp.listaLLamada(0,etiquetaFuncion)
            temp.listaRecusion(0,self.id)
            funcion.entorno = enLlamada
            funcion.etiqueta = etiquetaFuncion
            ventana.consola.appendPlainText("goto "+etiquetaFuncion+";")
            funcion.traducir(ent,arbol,ventana)
            ventana.consola.appendPlainText(etiquetaSalida+":")
            temp.listaLLamada(2,etiquetaFuncion)
            temp.listaRecusion(2,self.id)
        else:
            ventana.consola.appendPlainText("goto "+llamadaAnterior+";")

        
        