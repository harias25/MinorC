from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class Exit(Instruccion) :
    def __init__(self,linea,columna) :
        pass

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado

    def generarAugus(self):
        codigoAugus = "exit; \n"
        return codigoAugus