from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion ,OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class Unset(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado

    def generarAugus(self):
        codigoAugus = "unset("+self.id+");\n"
        return codigoAugus