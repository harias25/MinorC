from ast.Instruccion import Instruccion
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.AccesoStruct import AccesoStruct 
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor

    def traducir(self,ent,arbol,ventana):


        traduccionExpresion = self.valor.traducir(ent,arbol,ventana)
        if(traduccionExpresion == None): return None

        #acceso a struct
        if(isinstance(self.id,AccesoStruct)):
            acceso = self.id.traducir(ent,arbol,ventana)
            if(acceso == None): return None

            if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D)
            ventana.consola.appendPlainText(acceso.codigo3D + "="+traduccionExpresion.temporal.utilizar()+"; ") 
            return None


        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, no se encuentra declarado un identificador con el nombre "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        if(traduccionExpresion.codigo3D != ""): ventana.consola.appendPlainText(traduccionExpresion.codigo3D)

        
        traduccion = simbolo.temporal + "="+traduccionExpresion.temporal.utilizar()+"; "  

        try:
            ventana.consola.appendPlainText(traduccion) 
        except:
            pass