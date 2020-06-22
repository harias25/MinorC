from ast.Instruccion import Instruccion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
import ast.Temporales as Temp

class Scan(Instruccion) :
    def __init__(self,cad,id,linea,columna):
        self.cad = cad
        self.id = id
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        cadena3D = self.cad.traducir(ent,arbol)
        id3D = self.id.traducir(ent,arbol)

        if(cadena3D == None or id3D == None):
            return None

        ventana.consola.appendPlainText(id3D.temporal.obtener()+"=read();")