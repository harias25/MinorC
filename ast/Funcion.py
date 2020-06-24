from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
import ast.Entorno as TS
import ValorImplicito.Asignacion as Asignacion
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

class Funcion(Instruccion) :
    def __init__(self, tipo, id, instrucciones,parametros,linea,columna) :
        self.tipo = tipo
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
        self.parametros = parametros
        self.temporales = []
        self.entorno = None

    def inicializar(self,ent,arbol,ventana):
        self.entorno = TS.Entorno(ent)
        self.temporales = []
        for parametro in self.parametros:
            temporal = parametro.traducir(self.entorno,arbol,ventana)
            if(temporal != None): self.temporales.append(temporal)

    def traducir(self,ent,arbol,ventana):
        ventana.consola.appendPlainText(self.id+":")
        for ins in self.instrucciones:
            #try:
                ins.traducir(self.entorno,arbol,ventana)
            #except:
            #    pass

    def getTipo(self):
        return self.tipo.name