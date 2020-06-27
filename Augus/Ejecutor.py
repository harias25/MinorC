import Augus.ascendente as g
import Augus.ast.Entorno as TS
import Augus.ast.Instruccion as Instruccion
import Augus.ast.GoTo as GoTo
import Augus.ast.Declaracion as Declaracion
import Augus.Primitivas.Exit as Exit
import Augus.Condicionales.If as If
import Augus.ast.AST as AST
import Augus.Reporteria.Error as Error
import Augus.Reporteria.ReporteErrores as ReporteErrores
import Augus.Reporteria.ReporteTablaSimbolos as ReporteTablaSimbolos
import Augus.Reporteria.ReporteAST as ReporteAST
import Augus.ValorImplicito.Asignacion as Asignacion
import Augus.ValorImplicito.Conversion as Conversion
import Augus.Reporteria.ReporteGramatical as ReporteGramatical
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
import re
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import filedialog

class Ejecutor():
    def __init__(self):
        self.ts_global = TS.Entorno(None)
        self.ast =  AST.AST([]) 
        self.listado_gramatical = []
        self.instrucciones = []
        self.hilo_terminado = True

    def generarAST(self):
        reporteAST = ReporteAST.ReporteAST()
        reporteAST.graficar(self.instrucciones)

    def generarTabla(self):
        reporteTablas = ReporteTablaSimbolos.ReporteTablaSimbolos()
        reporteTablas.generarReporte(self.ts_global,self.ast)

    def generarRErrores(self):
        reporteErrores = ReporteErrores.ReporteErrores()
        reporteErrores.generarReporte()

    def generarRGramatical(self):
        listado = self.listado_gramatical 
        reporteGramatical = ReporteGramatical.ReporteGramatical()
        reporteGramatical.generarReporte(listado[0])

    def debugger(self,ventana):
        ventana.tableWidget.setRowCount(0)
        ventana.tableWidget.setRowCount(100)
        ventana.tableWidget.setItem(0,0, QTableWidgetItem("No."))
        ventana.tableWidget.setItem(0,1, QTableWidgetItem("Simbolo"))
        ventana.tableWidget.setItem(0, 2 , QTableWidgetItem("Valor"))

        if(self.hilo_terminado):
            sys.setrecursionlimit(2147483644)
            ventana.consola.clear()
            ReporteErrores.func(None,True)
            g.func(0,None)
            g.textoEntrada = ventana.editor.text()
            instrucciones = g.parse(ventana.editor.text())
            self.instrucciones = instrucciones
            ts_global = TS.Entorno(None)
            ast = AST.AST(instrucciones) 

            declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"","GLOBAL")
            declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"","GLOBAL")
            declaracion1.ejecutar(ts_global,ast,ventana,True)
            declaracion2.ejecutar(ts_global,ast,ventana,True)

            bandera = False
            if(instrucciones != None):
                for ins in instrucciones:
                    try:
                        if(bandera == False and ins.id != "main"):
                            error = Error.Error("SEMANTICO","Error semantico, La primera etiqueta debe ser la etiqueta main:",ins.linea,ins.columna)
                            ReporteErrores.func(error)
                            break
                        else:
                            bandera = True
                        if(ast.existeEtiqueta(ins)):
                            error = Error.Error("SEMANTICO","Error semantico, Ya existe la etiqueta "+ins.id,ins.linea,ins.columna)
                            ReporteErrores.func(error)
                        else:
                            ast.agregarEtiqueta(ins)
                    except:
                            pass
            self.ts_global = ts_global
            self.ast = ast
            self.listado_gramatical = g.func(1,None).copy()

            self.debug(ventana)

    def ascendente(self,ventana):
        sys.setrecursionlimit(2147483644)
        ventana.consola.clear()
        ReporteErrores.func(None,True)
        g.textoEntrada = ventana.editor.text()
        g.func(0,None)
        instrucciones = g.parse(ventana.editor.text())
        self.instrucciones = instrucciones
        ts_global = TS.Entorno(None)
        ts_global.asignarConsola(ventana.consola)
        ast = AST.AST(instrucciones) 

        declaracion1 = Declaracion.Declaracion('$ra',0,0,0,"","GLOBAL")
        declaracion2 = Declaracion.Declaracion('$sp',0,0,0,"","GLOBAL")
        declaracion1.ejecutar(ts_global,ast,ventana,False)
        declaracion2.ejecutar(ts_global,ast,ventana,False)


        #PRIMERA PASADA PARA GUARDAR TODAS LAS ETIQUETAS
        bandera = False
        if(instrucciones != None):
            for ins in instrucciones:
                try:
                    if(bandera == False and ins.id != "main"):
                        error = Error.Error("SEMANTICO","Error semantico, La primera etiqueta debe ser la etiqueta main:",ins.linea,ins.columna)
                        ReporteErrores.func(error)
                        break
                    else:
                        bandera = True
                    if(ast.existeEtiqueta(ins)):
                        error = Error.Error("SEMANTICO","Error semantico, Ya existe la etiqueta "+ins.id,ins.linea,ins.columna)
                        ReporteErrores.func(error)
                    else:
                        ast.agregarEtiqueta(ins)
                except:
                        pass

        main = ast.obtenerEtiqueta("main")

        if(main != None):
            salir = False
            for ins in main.instrucciones:
                try:
                    if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                        ins.setAmbito("main")

                    if(ins.ejecutar(ts_global,ast,ventana,False) == True):
                        salir = True
                        break
                except:
                    pass
            if(not salir):   
                siguiente = ast.obtenerSiguienteEtiqueta("main")
                if(siguiente!=None):
                    siguiente.ejecutar(ts_global,ast,ventana,False)
        else:
            error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe la etiqueta main:",0,0)
            ReporteErrores.func(error)

        listado = ReporteErrores.func(None)
        if(len(listado)>0):
            QMessageBox.critical(ventana.centralwidget, "Errores en Ejecución", "Se obtuvieron errores en la ejecución del Código Ingresado, verifique reporte de Errores")

        self.ts_global = ts_global
        self.ast = ast
        self.listado_gramatical = g.func(1,None).copy()

    def debug(self,ventana):
        self.hilo_terminado = False
        main = self.ast.obtenerEtiqueta("main")

        if(main != None):
            salir = False
            ventana.editor.setCursorPosition(0,0)
            ventana.editor.setFocus()
            time.sleep(2)
            for ins in main.instrucciones:
                QApplication.processEvents()
                try:
                    ventana.editor.setCursorPosition(ins.linea-1,0)
                    ventana.editor.setFocus()
                    time.sleep(2)
                    if(isinstance(ins,Asignacion.Asignacion) or isinstance(ins,Conversion.Conversion)):
                        ins.setAmbito("main")
                    if(ins.ejecutar(self.ts_global,self.ast,ventana,True) == True):
                        salir = True
                        break
                    
                    contador = 1
                    ventana.tableWidget.setRowCount(0)
                    ventana.tableWidget.setRowCount(100)
                    ventana.tableWidget.setItem(0,0, QTableWidgetItem("No."))
                    ventana.tableWidget.setItem(0,1, QTableWidgetItem("Simbolo"))
                    ventana.tableWidget.setItem(0, 2 , QTableWidgetItem("Valor"))
                    for key in self.ts_global.tabla:
                        s = self.ts_global.tabla[key]
                        ventana.tableWidget.setItem(contador,0, QTableWidgetItem(str(contador)))
                        ventana.tableWidget.setItem(contador,1, QTableWidgetItem(s.id))
                        ventana.tableWidget.setItem(contador, 2 , QTableWidgetItem(str(s.valor)))
                        contador = contador + 1 
                except:
                    pass
            
            if(not salir):   
                siguiente = self.ast.obtenerSiguienteEtiqueta("main")
                if(siguiente!=None):
                    siguiente.ejecutar(self.ts_global,self.ast,ventana,True)
        else:
            error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe la etiqueta main:",0,0)
            ReporteErrores.func(error)
        listado = ReporteErrores.func(None)
        if(len(listado)>0):
            QMessageBox.critical(ventana.centralwidget, "Errores en Ejecución", "Se obtuvieron errores en la ejecución del Código Ingresado, verifique reporte de Errores")
        self.hilo_terminado = True
        #print ("Terminado hilo ")