from Optimizador.OptimizadorAST.Expresion import Expresion
from Optimizador.OptimizadorAST.Simbolo import TIPO_DATO as Tipo
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class Primitivo(Expresion):
    def __init__(self,valor,linea,columna):
        self.valor          = valor     #Object
    
    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado

    def generarAugus(self):
        return str(self.valor)
    
