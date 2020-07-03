import Optimizador.grammarOptimizacion as g
import Optimizador.OptimizadorAST.Instruccion as Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion 
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion
from Optimizador.OptimizadorAST.AST import AST

class Optimizador():
    def __init__(self):
        self.codigoOptimizado = ""
        self.codigoAnterior = ""
        self.instrucciones = []

    def inicializar(self):
        ReporteOptimizacion.func(None, True)
        self.codigoOptimizado = ""
        self.codigoAnterior = ""
        self.instrucciones = []

    def optimizar(self, texto):
        self.codigoAnterior = texto
        self.codigoOptimizado = ""
        g.textoEntrada = texto
        g.func(0, None)
        instrucciones = g.parse(texto)
        self.instrucciones = instrucciones
        ast = AST(self.instrucciones)
        #PRIMERA PASADA PARA GUARDAR TODAS LAS ETIQUETAS
        if(instrucciones != None):
            for ins in instrucciones:
                try:
                    print(ins.id)
                    ast.agregarEtiqueta(ins)
                except:
                    pass

        if(instrucciones != None):
            for func in instrucciones:
                #try:
                    if(func.id in ast.etiquetasBetadas):
                        continue

                    self.codigoOptimizado +=func.optmimizarCodigo(ast)
                #except:
                #    pass

        return self.codigoOptimizado

    def reporte(self):
        reporte = ReporteOptimizacion.ReporteOptimizacion()
        reporte.ReporteOptimizacion()