from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorAST.Simbolo import TIPO_DATO as Tipo
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class Conversion(Instruccion):
    def __init__(self,id,valor,tipo,linea,columna):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.declarada = None

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes
        return resultado

    def generarAugus(self):
        codigoAugus = self.id+" = ("+self.tipo+") "+self.valor.generarAugus()+";\n"
        return codigoAugus