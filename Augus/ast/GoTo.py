from Augus.ast.Instruccion import Instruccion
import Augus.ast.Entorno as TS
import Augus.Primitivas.Exit as Exit
from Augus.Reporteria.Error import Error 
import Augus.Reporteria.ReporteErrores as ReporteErrores
#import pruebas

class GoTo(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol,ventana,isDebug):
        etiqueta = arbol.obtenerEtiqueta(self.id)

        if(etiqueta == None):
            error = Error("SEMANTICO","Error semantico, no existe la etiqueta "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
        else:
            etiqueta.ejecutar(ent,arbol,ventana,isDebug)
           # if(type(resultado) is Exit.Exit): 
            #    return resultado   
            return True

        return False