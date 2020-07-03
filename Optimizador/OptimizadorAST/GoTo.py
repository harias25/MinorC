from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion
#import pruebas

class GoTo(Instruccion) :
    def __init__(self,id,linea,columna) :
        self.id = id
        self.linea = linea
        self.columna = columna
        self.ast = None

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes
        return resultado

    def generarAugus(self):
        codigoAugus = "goto "+self.id+";\n"


        etiqueta = self.ast.obtenerEtiqueta(self.id)
        try:
            if(len(etiqueta.instrucciones)>0):
                #validacion de regla 6 Mirilla
                optimizacion = Optimizacion()
                optimizacion.linea = str(self.linea)
                optimizacion.antes = codigoAugus
                optimizacion.tipo = "Mirilla - Optimizaciones de flujo de control"
                optimizacion.regla = "Regla 6"
                if isinstance(etiqueta.instrucciones[0],GoTo):
                    codigoAugus = "goto "+etiqueta.instrucciones[0].id+";\n"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
        except:
            pass

        return codigoAugus