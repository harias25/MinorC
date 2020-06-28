from ast.Instruccion import Instruccion
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.AccesoStruct import AccesoStruct 
from ValorImplicito.AccesoLista import AccesoLista 
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna,tipo=""):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor
        self.tipo = tipo

    def traducir(self,ent,arbol,ventana):
        #acceso a struct
        if(isinstance(self.id,AccesoStruct) or isinstance(self.id,AccesoLista)):
            traduccionExpresion = self.valor.traducir(ent,arbol,ventana)
            if(traduccionExpresion == None): return None

            acceso = self.id.traducir(ent,arbol,ventana)
            if(acceso == None): return None

            if(traduccionExpresion.codigo3D != ""): ventana.editor.append("\n"+traduccionExpresion.codigo3D)
            if(isinstance(self.id,AccesoStruct)):
                ventana.editor.append("\n"+acceso.codigo3D + "="+self.tipo+traduccionExpresion.temporal.utilizar()+"; ") 
            else:
                ventana.editor.append("\n"+acceso.temporal.utilizar() + "="+self.tipo+traduccionExpresion.temporal.utilizar()+"; ") 

            return None

        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, no se encuentra declarado un identificador con el nombre "+self.id,self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        
        if(simbolo.llaves!=None): #array
            if(isinstance(self.valor,list)):
                self.operacionesArray(ent,arbol,ventana,self.valor,simbolo.temporal,"")
            else:
                traduccionExpresion = self.valor.traducir(ent,arbol,ventana)
                if(traduccionExpresion == None): return None

                if(simbolo.tipo == Tipo.CHAR and traduccionExpresion.tipo == Tipo.CHAR):
                    if(traduccionExpresion.codigo3D != ""): ventana.editor.append("\n"+traduccionExpresion.codigo3D)
                    traduccion = simbolo.temporal + "="+self.tipo+traduccionExpresion.temporal.utilizar()+"; "  
                    ventana.editor.append("\n"+traduccion) 
                else:
                    error = Error("SEMANTICO","Error semantico, expresión incorrecta al asignar el Arrray "+self.id,self.linea,self.columna)
                    ReporteErrores.func(error)
                    return None

        else:
            if(isinstance(self.valor,list)):
                error = Error("SEMANTICO","Error semantico, expresión incorrecta para asignar el identificador "+self.id,self.linea,self.columna)
                ReporteErrores.func(error)
                return None

            traduccionExpresion = self.valor.traducir(ent,arbol,ventana)
            if(traduccionExpresion == None): return None

            if(traduccionExpresion.codigo3D != ""): ventana.editor.append("\n"+traduccionExpresion.codigo3D)

            
            traduccion = simbolo.temporal + "="+self.tipo+traduccionExpresion.temporal.utilizar()+"; "  

            try:
                ventana.editor.append("\n"+traduccion) 
            except:
                pass


    def operacionesArray(self,ent,arbol,ventana,lista,temporal,niveles):
        contador = 0
        for valor in lista:
            if(isinstance(valor,list)): #otro nivel
                niveles="["+str(contador)+"]"
                self.operacionesArray(ent,arbol,ventana,valor,temporal,niveles)
            else:
                traduccionExpresion = valor.traducir(ent,arbol,ventana)
                if(traduccionExpresion == None): return None
                if(traduccionExpresion.codigo3D != ""): ventana.editor.append("\n"+traduccionExpresion.codigo3D)

                ventana.editor.append("\n"+temporal+niveles+"["+str(contador)+"]="+self.tipo+traduccionExpresion.temporal.obtener()+";")
            
            contador = contador + 1
                