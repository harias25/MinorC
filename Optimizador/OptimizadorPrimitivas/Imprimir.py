from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion
                        
class Imprimir(Instruccion) :
    def __init__(self,cad,linea,columna):
        self.cad = cad
        self.linea = linea
        self.columna = columna

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado

    def generarAugus(self):
        codigoAugus = "print("+self.cad.generarAugus()+");\n"
        return codigoAugus
