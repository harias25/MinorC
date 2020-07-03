#Clase principal para el manejo de los simbolos que soportará el programa
from enum import Enum
from Optimizador.OptimizadorAST.Expresion import Expresion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class TIPO_DATO(Enum) :
    ENTERO = 1,
    DOOBLE = 2,
    STRING = 3,
    BOOLEAN = 4,
    NULL = 5

class Simbolo(Expresion) :
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
        return self.id