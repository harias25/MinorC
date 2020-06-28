from ValorImplicito.Primitivo import Primitivo
from ast.Instruccion import Instruccion
from ast.Expresion import Expresion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
from ast.Temporales import Resultado3D
from ast.Temporales import Temporal

class AccesoLista(Expresion,Instruccion):
    def __init__(self,id,llaves,valor,linea,columna):
        self.id             = id    
        self.llaves         = llaves  
        self.linea          = linea
        self.columna        = columna

    def traducir(self,ent,arbol,ventana):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, No existe la variable con identificador "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        strAccesos = ""
        for llave in self.llaves:
            expresion = llave.traducir(ent,arbol,ventana)
            if(expresion == None): return None

            if(expresion.codigo3D != ""): ventana.editor.append("\n"+expresion.codigo3D)
            strAccesos +="["+expresion.temporal.utilizar()+"]"

        resultado3D = Resultado3D()
        resultado3D.codigo3D = ""
        resultado3D.tipo = simbolo.tipo
        resultado3D.temporal = Temporal(simbolo.temporal+strAccesos)
        return resultado3D
    
    
