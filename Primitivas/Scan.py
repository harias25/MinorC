from ast.Instruccion import Instruccion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as Temp
from ast.Declaracion import Declaracion

class Scan(Instruccion) :
    def __init__(self,tipo,id,linea,columna):
        self.tipo = tipo
        self.id = id
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        #cadena3D = self.cad.traducir(ent,arbol,ventana)

        if(self.tipo!=None):
            declaracion = Declaracion(self.tipo,[self.id.valor],None,self.linea,self.columna)
            declaracion.traducir(ent,arbol,ventana)

        
        id3D = self.id.traducir(ent,arbol,ventana)
        if(id3D == None):
            return None
        ventana.editor.append("\n"+id3D.temporal.obtener()+"=read();")