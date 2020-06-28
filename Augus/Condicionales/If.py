from Augus.ast.Instruccion import Instruccion
import Augus.ast.Entorno as TS
from Augus.Reporteria.Error import Error 
import Augus.Reporteria.ReporteErrores as ReporteErrores
import Augus.Primitivas.Exit as Exit

class If(Instruccion) :
    def __init__(self,  condicion, instruccionV,linea,columna) :
        self.condicion = condicion
        self.instruccionV = instruccionV
        self.linea = linea
        self.columna = columna

    def ejecutar(self,ent,arbol,ventana,isDebug):
        resultado = self.condicion.getValorImplicito(ent,arbol)
        if(resultado == 0 or resultado == 0.0): resultado = False
        if(resultado == 1 or resultado == 1.0): resultado = True

        if(not isinstance(resultado,bool)):
            error = Error("SEMANTICO","Error semantico, Se esperaba un valor 1 o 0 para validar el IF.",self.linea,self.columna)
            ReporteErrores.func(error)

        if(bool(resultado)):
            try:
               return self.instruccionV.ejecutar(ent,arbol,ventana,isDebug)
            except:
                return False

        return False
        