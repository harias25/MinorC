from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorAST.Expresion import Expresion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class AccesoLista(Expresion,Instruccion):
    def __init__(self,id,llaves,valor,linea,columna,DefArray):
        self.id             = id    
        self.llaves         = llaves  
        self.linea          = linea
        self.columna        = columna
        self.asignacion     = valor
        self.defArray       = DefArray
    

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes;
        return resultado

    def generarAugus(self):
        codigoAugus = self.id
        for llave in self.llaves:
            codigoAugus+="["+llave.generarAugus()+"]"

        if(self.asignacion!=None):
            codigoAugus = codigoAugus+" = "+self.asignacion.generarAugus()+";\n"

        return codigoAugus
        