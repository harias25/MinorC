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
import gramatica as g
import ast.Entorno as TS
import ast.Instruccion as Instruccion
import ast.Declaracion as Declaracion
import ast.AST as AST
from ast.Funcion import Funcion
from ast.Struct import Struct
import Reporteria.Error as Error
import Reporteria.ReporteErrores as ReporteErrores
import Reporteria.ReporteTablaSimbolos as ReporteTablaSimbolos
import Reporteria.ReporteAST as ReporteAST
import ValorImplicito.Asignacion as Asignacion
import Reporteria.ReporteGramatical as ReporteGramatical
import ast.Temporales as temp
from Augus.Ejecutor import Ejecutor
from Optimizador.Optimizador import Optimizador

class Ui_MainWindow(object):

    resultChanged = QtCore.pyqtSignal(str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1240, 720)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frameCodigo = QtWidgets.QFrame(self.centralwidget)
        self.frameCodigo.setGeometry(QtCore.QRect(0, 30, 740, 450))
        self.frameCodigo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameCodigo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameCodigo.setObjectName("frameCodigo")


        self.frame3D = QtWidgets.QFrame(self.centralwidget)
        self.frame3D.setGeometry(QtCore.QRect(740, 30, 495, 425))
        self.frame3D.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame3D.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame3D.setObjectName("frame3D")
        
        self.frameConsola = QtWidgets.QFrame(self.centralwidget)
        self.frameConsola.setGeometry(QtCore.QRect(0, 480, 730, 200))
        self.frameConsola.setAutoFillBackground(True)
        self.frameConsola.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameConsola.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameConsola.setObjectName("frameConsola")

        self.scrollDebug = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollDebug.setGeometry(QtCore.QRect(750, 450, 475, 250))
        self.scrollDebug.setWidgetResizable(False)
        self.scrollDebug.setObjectName("scrollDebug")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 520, 300))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 520, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.scrollDebug.setWidget(self.scrollAreaWidgetContents)

        self.consola = QtWidgets.QPlainTextEdit(self.frameConsola)
        self.consola.setGeometry(QtCore.QRect(10, 0, 890, 200))

        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)


        font2 = QtGui.QFont()
        font2.setFamily("Consolas")
        font2.setPointSize(13)
        font2.setBold(True)
        font2.setWeight(100)
        font2.setKerning(True)


        self.consola.setFont(font2)
        self.consola.setAutoFillBackground(False)
        #self.consola.setTextFormat(QtCore.Qt.RichText)
        self.consola.setObjectName("consola")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-1, 0, 1001, 31))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1011, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuPrograma = QtWidgets.QMenu(self.menubar)
        self.menuPrograma.setObjectName("menuPrograma")
        self.menuReportes = QtWidgets.QMenu(self.menubar)
        self.menuReportes.setObjectName("menuReportes")

        self.menuReportes2 = QtWidgets.QMenu(self.menubar)
        self.menuReportes2.setObjectName("menuReportes2")

        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNuevo = QtWidgets.QAction(MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionArbir = QtWidgets.QAction(MainWindow)
        self.actionArbir.setObjectName("actionArbir")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_Como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_Como.setObjectName("actionGuardar_Como")
        self.actionCerrrar = QtWidgets.QAction(MainWindow)
        self.actionCerrrar.setObjectName("actionCerrrar")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionCopiar = QtWidgets.QAction(MainWindow)
        self.actionCopiar.setObjectName("actionCopiar")
        self.actionPegar = QtWidgets.QAction(MainWindow)
        self.actionPegar.setObjectName("actionPegar")
        self.actionCortar = QtWidgets.QAction(MainWindow)
        self.actionCortar.setObjectName("actionCortar")
        self.actionBuscar = QtWidgets.QAction(MainWindow)
        self.actionBuscar.setObjectName("actionBuscar")
        self.actionReemplazar = QtWidgets.QAction(MainWindow)
        self.actionReemplazar.setObjectName("actionReemplazar")


        self.actionTraducir = QtWidgets.QAction(MainWindow)
        self.actionTraducir.setObjectName("actionTraducir")

        self.actionTraducirOptimizado = QtWidgets.QAction(MainWindow)
        self.actionTraducirOptimizado.setObjectName("actionTraducirOptimizado")

        self.actionEjecutar_Ascendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Ascendente.setObjectName("actionEjecutar_Ascendente")

        self.actionEjecutarOptimizado = QtWidgets.QAction(MainWindow)
        self.actionEjecutarOptimizado.setObjectName("actionEjecutarOptimizado")

        self.actionEjecutarAugus = QtWidgets.QAction(MainWindow)
        self.actionEjecutarAugus.setObjectName("actionEjecutarOptimizado")

        self.actionEjecutar_Paso_a_Paso_Ascendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Paso_a_Paso_Ascendente.setObjectName("actionEjecutar_Paso_a_Paso_Ascendente")

        self.actionTabla_de_Simbolos = QtWidgets.QAction(MainWindow)
        self.actionTabla_de_Simbolos.setObjectName("actionTabla_de_Simbolos")
        self.actionErrores = QtWidgets.QAction(MainWindow)
        self.actionErrores.setObjectName("actionErrores")
        self.actionAST = QtWidgets.QAction(MainWindow)
        self.actionAST.setObjectName("actionAST")
        self.actionGramatical = QtWidgets.QAction(MainWindow)
        self.actionGramatical.setObjectName("actionGramatical")
        self.actionOptmizacion = QtWidgets.QAction(MainWindow)
        self.actionOptmizacion.setObjectName("actionOptmizacion")

        self.actionTabla_de_Simbolos2 = QtWidgets.QAction(MainWindow)
        self.actionTabla_de_Simbolos2.setObjectName("actionTabla_de_Simbolos")
        self.actionErrores2 = QtWidgets.QAction(MainWindow)
        self.actionErrores2.setObjectName("actionErrores")
        self.actionAST2 = QtWidgets.QAction(MainWindow)
        self.actionAST2.setObjectName("actionAST")
        self.actionGramatical2 = QtWidgets.QAction(MainWindow)
        self.actionGramatical2.setObjectName("actionGramatical")

        self.actionAyuda = QtWidgets.QAction(MainWindow)
        self.actionAyuda.setObjectName("actionAyuda")
        self.actionAcercaDe = QtWidgets.QAction(MainWindow)
        self.actionAcercaDe.setObjectName("actionAcercaDe")

        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionArbir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_Como)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionCerrrar)
        self.menuArchivo.addAction(self.actionSalir)

        self.menuPrograma.addAction(self.actionEjecutar_Ascendente)
        self.menuPrograma.addAction(self.actionEjecutarOptimizado)
        self.menuPrograma.addSeparator()

        self.menuPrograma.addAction(self.actionTraducir)
        self.menuPrograma.addAction(self.actionTraducirOptimizado)

        self.menuPrograma.addSeparator()
        self.menuPrograma.addAction(self.actionEjecutar_Paso_a_Paso_Ascendente)
        self.menuPrograma.addSeparator()
        self.menuPrograma.addAction(self.actionEjecutarAugus)

        self.menuReportes.addAction(self.actionTabla_de_Simbolos)
        self.menuReportes.addAction(self.actionErrores)
        self.menuReportes.addAction(self.actionAST)
        self.menuReportes.addAction(self.actionGramatical)
        self.menuReportes.addAction(self.actionOptmizacion)


        self.menuReportes2.addAction(self.actionTabla_de_Simbolos2)
        self.menuReportes2.addAction(self.actionErrores2)
        self.menuReportes2.addAction(self.actionAST2)
        self.menuReportes2.addAction(self.actionGramatical2)

        self.menuAyuda.addAction(self.actionAyuda)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuPrograma.menuAction())
        self.menubar.addAction(self.menuReportes.menuAction())
        self.menubar.addAction(self.menuReportes2.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())


        self.__myFont = QFont()
        self.__myFont.setPointSize(12)

        #************************************************ REGLAS DEL LENGUAJE MINOR C *****************************************
        self.codigo = QsciScintilla()
        self.codigo.setText("")              
        self.codigo.setLexer(None)           
        self.codigo.setUtf8(True)             
        self.codigo.setFont(self.__myFont)    

        #AJUSTES DE TEXTO
        self.codigo.setWrapMode(QsciScintilla.WrapWord)
        self.codigo.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.codigo.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

        #FIN DE LINEA
        self.codigo.setEolMode(QsciScintilla.EolWindows)
        self.codigo.setEolVisibility(False)

        #SANGRIA
        self.codigo.setIndentationsUseTabs(False)
        self.codigo.setTabWidth(4)
        self.codigo.setIndentationGuides(True)
        self.codigo.setTabIndents(True)
        self.codigo.setAutoIndent(True)

        self.codigo.setCaretForegroundColor(QColor("#ff0000ff"))
        self.codigo.setCaretLineVisible(True)
        self.codigo.setCaretLineBackgroundColor(QColor("#1f0000ff"))
        self.codigo.setCaretWidth(2)

        # MARGENES
        self.codigo.setMarginType(0, QsciScintilla.NumberMargin)
        self.codigo.setMarginWidth(0, "0000")  #con este se puede quitar la linea
        self.codigo.setMarginsForegroundColor(QColor("#ff888888"))

        #SE COLOCAN LAS REGLAS DEL EDITOR
        self.__lexer = QsciLexerCPP(self.codigo)
        self.codigo.setLexer(self.__lexer)

        self.__lyt = QVBoxLayout()
        self.frameCodigo.setLayout(self.__lyt)
        self.__lyt.addWidget(self.codigo)


         #************************************************ REGLAS DEL LENGUAJE AUGUS *****************************************
        self.editor = QsciScintilla()
        self.editor.setText("")              
        self.editor.setLexer(None)           
        self.editor.setUtf8(True)             
        self.editor.setFont(self.__myFont)    

        #AJUSTES DE TEXTO
        self.editor.setWrapMode(QsciScintilla.WrapWord)
        self.editor.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.editor.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

        #FIN DE LINEA
        self.editor.setEolMode(QsciScintilla.EolWindows)
        self.editor.setEolVisibility(False)

        #SANGRIA
        self.editor.setIndentationsUseTabs(False)
        self.editor.setTabWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(True)

        self.editor.setCaretForegroundColor(QColor("#ff0000ff"))
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#1f0000ff"))
        self.editor.setCaretWidth(2)

        # MARGENES
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")  #con este se puede quitar la linea
        self.editor.setMarginsForegroundColor(QColor("#ff888888"))

        #SE COLOCAN LAS REGLAS DEL EDITOR
        self.__lexer2 = QsciLexerRuby(self.editor)
        self.editor.setLexer(self.__lexer2)

        self.__lyt2 = QVBoxLayout()
        self.frame3D.setLayout(self.__lyt2)
        self.__lyt2.addWidget(self.editor)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionNuevo.triggered.connect(self.clean)
        self.actionArbir.triggered.connect(self.open)
        self.actionGuardar.triggered.connect(self.save)
        self.actionGuardar_Como.triggered.connect(self.save_as)
        self.actionCerrrar.triggered.connect(self.clear)
        self.actionSalir.triggered.connect(self.exit)
        self.ruta_archivo  = None

        self.actionEjecutar_Ascendente.triggered.connect(self.ejecutar)
        self.actionEjecutarOptimizado.triggered.connect(self.ejecutarOptmizado)

        self.actionTraducir.triggered.connect(self.traducir)
        self.actionTraducirOptimizado.triggered.connect(self.optimizar)

        self.actionEjecutarAugus.triggered.connect(self.ejecutarAugus)

        self.actionEjecutar_Paso_a_Paso_Ascendente.triggered.connect(self.debug)

        self.actionTabla_de_Simbolos.triggered.connect(self.generarTabla)
        self.actionErrores.triggered.connect(self.generarRErrores)
        self.actionGramatical.triggered.connect(self.generarRGramatical)
        self.actionAST.triggered.connect(self.generarAST)
        
        self.actionTabla_de_Simbolos2.triggered.connect(self.generarTabla2)
        self.actionErrores2.triggered.connect(self.generarRErrores2)
        self.actionGramatical2.triggered.connect(self.generarRGramatical2)
        self.actionAST2.triggered.connect(self.generarAST2)

        self.actionOptmizacion.triggered.connect(self.generarReporteOptmizacion)

        self.actionAcercaDe.triggered.connect(self.acercade)
        self.actionAyuda.triggered.connect(self.ayuda)

        self.ts_global = TS.Entorno(None)
        self.ast =  AST.AST([]) 
        self.listado_gramatical = []
        self.instrucciones = []

        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(0,0, QTableWidgetItem("No."))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Simbolo"))
        self.tableWidget.setItem(0, 2 , QTableWidgetItem("Valor"))

        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 160)
        self.tableWidget.setColumnWidth(2, 250)

        self.consola.setStyleSheet("background-color: black;border: 1px solid black;color:green;") 

        self.ejecutor = Ejecutor()
        self.optimizador = Optimizador()
        #self.consola.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

    def clean(self):
        self.ruta_archivo = None
        self.editor.setText("")
        self.codigo.setText("")
        self.consola.clear()

    def generarReporteOptmizacion(self):
        self.optimizador.reporte()

    def optimizar(self):
        self.traducir()
        self.optimizador = Optimizador()
        self.optimizador.inicializar()
        codigo = self.optimizador.optimizar(self.editor.text())
        codigo2 =self.optimizador.optimizar(codigo)
        self.editor.clear()
        self.editor.append(codigo2)

    def acercade(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("MINOR C IDE\nPrimer Proyecto Compiladores 2 Vacaciones Junio\nElaborado por: Haroldo Arias\nCarnet: 201020247")
        msg.setInformativeText("Python 3.8.3\nPLY\nPyQT\nScintilla")
        msg.setWindowTitle("Acerca de")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def ayuda(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("MINOR C IDE")
        msg.setInformativeText("Puedes encontrar el manual de este proyecto en:\nhttps://tinyurl.com/yabg9why")
        msg.setWindowTitle("Ayuda")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def setTexto(self,texto):
        self.consola.setText(self.consola.text() + texto)

    def debug(self):
        self.traduccion()
        self.ejecutor = Ejecutor()
        self.ejecutor.debugger(self)

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

    def generarAST2(self):
        self.ejecutor.generarAST()

    def generarTabla2(self):
        self.ejecutor.generarTabla()

    def generarRErrores2(self):
       self.ejecutor.generarRErrores()

    def generarRGramatical2(self):
        self.ejecutor.generarRGramatical()

    def traduccion(self):
        if self.codigo.text() == "":
            return 

        self.editor.setText("")
        sys.setrecursionlimit(2147483644)
        self.consola.clear()
        ReporteErrores.func(None,True)
        g.textoEntrada = self.codigo.text()
        g.func(0,None)
        instrucciones = g.parse(self.codigo.text())
        self.instrucciones = instrucciones
        ts_global = TS.Entorno(None)
        ast = AST.AST(instrucciones) 
        temp.temporal(True)
        temp.parametro(True)
        temp.etiqueta(True)
        temp.listaContinue(-1,None)
        temp.listaBreak(-1,None)
        temp.listaReturn(-1,None)
        temp.listaLLamada(-1,None)
        temp.listaRecusion(-1,None)

        #PRIMERA PASADA PARA GUARDAR TODAS LAS FUNCIONES Y STRUCTS
        if(instrucciones != None):
            for ins in instrucciones:
                try:
                    if(isinstance(ins,Funcion)): 
                        if(ast.existeEtiqueta(ins)):
                            error = Error.Error("SEMANTICO","Error semantico, Ya existe la funcion "+ins.id,ins.linea,ins.columna)
                            ReporteErrores.func(error)
                        else:
                            if(ins.id != "main"):
                                ins.inicializar(ts_global,ast,self)
                            ast.agregarEtiqueta(ins)
                    elif(isinstance(ins,Struct)):
                        if(ast.existeStruct(ins)):
                            error = Error.Error("SEMANTICO","Error semantico, Ya existe el Struct "+ins.id,ins.linea,ins.columna)
                            ReporteErrores.func(error)
                        else:
                            ast.agregarStruct(ins)
                except:
                        pass

        #SE TRADUCE EL METODO MAIN
        main = ast.obtenerEtiqueta("main")

        if(main != None):
            self.editor.append("main:")

            #se corren las instrucciones globales
            for ins in instrucciones:
                try:
                    if(not isinstance(ins,Funcion)): 
                        try:
                            ins.traducir(ts_global,ast,self)
                        except:
                            pass
                except:
                        pass
            entMain = TS.Entorno(ts_global)             
            for ins in main.instrucciones:
                try:
                    ins.traducir(entMain,ast,self)
                except:
                    pass
        else:
            error = Error.Error("SEMANTICO","Error semantico, No puede iniciarse el programa ya que no existe el metodo main()",0,0)
            ReporteErrores.func(error)

        #SE TRADUCEN LAS DEMAS FUNCIONES
        #if(instrucciones != None):
        #    for ins in instrucciones:
                #try:
        #            if(isinstance(ins,Funcion)): 
        #                if(ins.id!="main"):
        #                   ins.traducir(ts_global,ast,self)
                #except:
                #        pass

        listado = ReporteErrores.func(None)
        if(len(listado)>0):
            QMessageBox.critical(self.centralwidget, "Errores en Traducción", "Se obtuvieron errores en la traducción del Código Ingresado, verifique reporte de Errores de Traducción")

        self.ts_global = ts_global
        self.ast = ast
        self.listado_gramatical = g.func(1,None).copy()

    def ejecutarAugus(self):
        self.ejecutor = Ejecutor()
        self.ejecutor.ascendente(self)

    def traducir(self):
        self.traduccion()
        
    def ejecutar(self):
        self.optimizador = Optimizador()
        self.traducir()
        self.ejecutarAugus()

    def ejecutarOptmizado(self):
        self.traducir()
        self.optimizar()
        self.ejecutarAugus()

    def exit(self):
        sys.exit()

    def clear(self):
        self.ruta_archivo = None
        self.editor.setText("")
        self.codigo.setText("")
        self.consola.clear()

    def open(self):
        root = tk.Tk()
        root.withdraw()
        ruta = filedialog.askopenfilename(title="Seleccione un archivo de Entrada")
        if not ruta: return
        try:
            f = open(ruta,"r")
            input = f.read()
            self.codigo.setText(input)
            f.close()
            self.ruta_archivo = ruta
        except Exception as e:
            raise
            QMessageBox.critical(self.centralwidget,'Error Cargando el Archivo', 'No es posible abrir el archivo: %r' % ruta)

    def save(self):
        if(self.ruta_archivo==None):
            root = tk.Tk()
            root.withdraw()
            ruta = filedialog.asksaveasfilename(title="Seleccione la ruta donde desea guardar el Archivo",filetypes=[('all files', '.*'), ('text files', '.txt')])
        else:
            ruta = self.ruta_archivo
        if not ruta: return
        try:
            f = open(ruta,"w")
            f.write(self.codigo.text())
            f.close()
        except Exception as e:
            raise
            QMessageBox.critical(self.centralwidget,'Error Guardando el Archivo', 'No es posible guardar el archivo: %r' % ruta)

    def save_as(self):
        ruta = filedialog.asksaveasfilename(title="Seleccione la ruta donde desea guardar el Archivo",filetypes=[('all files', '.*'), ('text files', '.txt')])
        if not ruta: return
        try:
            f = open(ruta,"w")
            f.write(self.codigo.text())
            f.close()
            self.ruta_archivo = ruta
        except Exception as e:
            raise
            QMessageBox.critical(self.centralwidget,'Error Guardando el Archivo', 'No es posible guardar el archivo: %r' % ruta)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IDE MINOR C - HAROLDO PABLO ARIAS MOLINA - 201020247"))
        #self.consola.setText(_translate("MainWindow", ""))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuPrograma.setTitle(_translate("MainWindow", "Programa"))
        self.menuReportes.setTitle(_translate("MainWindow", "Reportes Traductor"))
        self.menuReportes2.setTitle(_translate("MainWindow", "Reportes Ejecución"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionArbir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_Como.setText(_translate("MainWindow", "Guardar Como"))
        self.actionCerrrar.setText(_translate("MainWindow", "Cerrrar"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))

        self.actionEjecutar_Ascendente.setText(_translate("MainWindow", "Traducir y Ejecutar"))
        self.actionEjecutarOptimizado.setText(_translate("MainWindow", "Traducir, Optimizar y Ejecutar"))

        self.actionTraducir.setText(_translate("MainWindow", "Traducir"))
        self.actionTraducirOptimizado.setText(_translate("MainWindow", "Traducir y Optimizar"))

        self.actionEjecutarAugus.setText(_translate("MainWindow", "Ejecutar Augus"))

        self.actionEjecutar_Paso_a_Paso_Ascendente.setText(_translate("MainWindow", "Debugger 3D"))
        self.actionTabla_de_Simbolos.setText(_translate("MainWindow", "Tabla de Simbolos"))
        self.actionErrores.setText(_translate("MainWindow", "Errores"))
        self.actionAST.setText(_translate("MainWindow", "AST"))
        self.actionGramatical.setText(_translate("MainWindow", "Gramatical"))
        self.actionOptmizacion.setText(_translate("MainWindow", "Optmización"))

        self.actionTabla_de_Simbolos2.setText(_translate("MainWindow", "Tabla de Simbolos"))
        self.actionErrores2.setText(_translate("MainWindow", "Errores"))
        self.actionAST2.setText(_translate("MainWindow", "AST"))
        self.actionGramatical2.setText(_translate("MainWindow", "Gramatical"))

        self.actionAyuda.setText(_translate("MainWindow", "Ayuda"))
        self.actionAcercaDe.setText(_translate("MainWindow", "Acerca de"))

interfaz = None

def getUI():
    global interfaz
    return interfaz.consola

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10**9)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(MainWindow.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    interfaz = ui
    MainWindow.show()
    sys.exit(app.exec_())

