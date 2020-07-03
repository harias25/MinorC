from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorAST.Simbolo import TIPO_DATO as Tipo
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion
from Optimizador.OptimizadorValorImplicito.Operacion import TIPO_OPERACION

class Asignacion(Instruccion):
    def __init__(self,id,valor,linea,columna,parametro):
        self.linea = linea
        self.columna = columna
        self.id = id
        self.valor = valor
        self.parametro = parametro
        self.instruccionPrevia = None

    def optmimizarCodigo(self):
        antes = self.generarAugus()
        resultado = OptmizacionResultado()
        resultado.codigo = antes
        return resultado

    def generarAugus(self):
        if(self.parametro):
            codigoAugus = self.id+" = &"+self.valor.generarAugus()+";\n"
        else:
            codigoAugus = self.id+" = "+self.valor.generarAugus()+";\n"
            optimizacion = Optimizacion()
            optimizacion.linea = str(self.linea)
            optimizacion.antes = codigoAugus
            optimizacion.tipo = "Mirilla - Simplificación algebraica y por fuerza"

            if(self.valor.tipo == TIPO_OPERACION.SUMA):
                if(self.valor.validarRegla8(self.id)):
                    optimizacion.regla = "Regla 8"
                    optimizacion.despues = ""
                    ReporteOptimizacion.func(optimizacion)
                    return ""
                elif(self.valor.validarRegla12()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla12()+";\n"
                    optimizacion.regla = "Regla 12"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
            elif(self.valor.tipo == TIPO_OPERACION.RESTA):
                if(self.valor.validarRegla9(self.id)):
                    optimizacion.regla = "Regla 9"
                    optimizacion.despues = ""
                    ReporteOptimizacion.func(optimizacion)
                    return ""
                elif(self.valor.validarRegla13()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla13()+";\n"
                    optimizacion.regla = "Regla 13"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
            elif(self.valor.tipo == TIPO_OPERACION.MULTIPLICACION):
                if(self.valor.validarRegla10(self.id)):
                    optimizacion.regla = "Regla 10"
                    optimizacion.despues = ""
                    ReporteOptimizacion.func(optimizacion)
                    return ""
                elif(self.valor.validarRegla14()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla14()+";\n"
                    optimizacion.regla = "Regla 14"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
                elif(self.valor.validarRegla16()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla16()+";\n"
                    optimizacion.regla = "Regla 16"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
                elif(self.valor.validarRegla17()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla17()+";\n"
                    optimizacion.regla = "Regla 17"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
            elif(self.valor.tipo == TIPO_OPERACION.DIVISION):
                if(self.valor.validarRegla11(self.id)):
                    optimizacion.regla = "Regla 11"
                    optimizacion.despues = ""
                    ReporteOptimizacion.func(optimizacion)
                    return ""
                elif(self.valor.validarRegla15()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla15()+";\n"
                    optimizacion.regla = "Regla 15"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
                elif(self.valor.validarRegla18()!=""):
                    codigoAugus = self.id+" = "+self.valor.validarRegla18()+";\n"
                    optimizacion.regla = "Regla 18"
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
            elif(self.valor.tipo == TIPO_OPERACION.ID):
                codigoAugus = self.id+" = "+self.valor.generarAugus()+";\n"
                if self.instruccionPrevia !=None:
                    if self.instruccionPrevia.valor.tipo == TIPO_OPERACION.ID:
                        if(self.valor.validarRegla1(self.id,self.valor.valor,self.instruccionPrevia.id,self.instruccionPrevia.valor.valor)):
                            optimizacion.tipo = "Mirilla - Eliminación de Instrucciones Redundantes y de Almacenamiento"
                            optimizacion.regla = "Regla 1"
                            optimizacion.despues = ""
                            ReporteOptimizacion.func(optimizacion)
                            return ""
            else:
                codigoAugus = self.id+" = "+self.valor.generarAugus()+";\n"

        return codigoAugus