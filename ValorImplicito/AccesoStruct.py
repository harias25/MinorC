from ast.Instruccion import Instruccion
import ast.Temporales as temp
from ast.Temporales import Temporal
from ast.Temporales import Resultado3D
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
from ast.Simbolo import TIPO_DATO as Tipo

class AccesoStruct(Instruccion):
    def __init__(self,id,llave,linea,columna):
        self.id  = id    
        self.llave = llave
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        simbolo = ent.obtener(str(self.id))
        if(simbolo == None):
            error = Error("SEMANTICO","Error semantico, No es existe la variable "+str(self.id),self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        if(simbolo.tipo == Tipo.DOOBLE or simbolo.tipo == Tipo.ENTERO or simbolo.tipo == Tipo.FLOAT or simbolo.tipo == Tipo.CHAR):
            error = Error("SEMANTICO","Error semantico, La variable "+str(self.id)+" no es un Struct.",self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        
        struct = arbol.obtenerStruct(simbolo.tipo)
        if(struct == None):
            error = Error("SEMANTICO","Error semantico, El struct "+str(simbolo.tipo)+" no se encuentra definido.",self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        bandera = False
        for declaracion in struct.declaraciones:
            #if(simbolo.tipo == Tipo.DOOBLE or simbolo.tipo == Tipo.ENTERO or simbolo.tipo == Tipo.FLOAT or simbolo.tipo == Tipo.CHAR):  #primitivos basicos
            if(declaracion.lista[0] == self.llave): 
                bandera = True
                break

        if(not bandera):
            error = Error("SEMANTICO","Error semantico, El struct "+str(simbolo.tipo)+" no tiene definido el atributo "+self.llave,self.linea,self.columna)
            ReporteErrores.func(error)
            return None

        temporal = temp.nuevoTemporal()

        resultado3D = Resultado3D()
        resultado3D.codigo3D = simbolo.temporal+"[\""+self.llave+"\"]"
        resultado3D.tipo = simbolo.tipo
        resultado3D.temporal = temporal
        return resultado3D