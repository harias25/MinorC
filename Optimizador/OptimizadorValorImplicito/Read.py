from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class Read(Instruccion):
    def __init__(self,id,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
    
    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado

    def generarAugus(self):
        codigoAugus = self.id+"=read();\n"
        return codigoAugus