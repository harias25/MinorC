from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion , OptmizacionResultado
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion
from Optimizador.OptimizadorValorImplicito.Operacion import TIPO_OPERACION
from Optimizador.OptimizadorAST.GoTo import GoTo

class If(Instruccion) :
    def __init__(self,  condicion, etiqueta,linea,columna) :
        self.condicion = condicion
        self.etiqueta = etiqueta
        self.linea = linea
        self.columna = columna
        self.instrucciones = []

    def optmimizarCodigo(self,ast):
        antes = self.generarAugus(ast)
        resultado = OptmizacionResultado()
        resultado.codigo = antes
        return resultado

    def generarAugus(self,ast):
        codigoAugus = "if( "+self.condicion.generarAugus()+" ) goto "+self.etiqueta+";\n"
        optimizacion = Optimizacion()
        optimizacion.linea = str(self.linea)
        optimizacion.antes = codigoAugus
        optimizacion.tipo = "Mirilla - Eliminación de Codigo Inalcanzable"


        
        if(self.condicion.tipo == TIPO_OPERACION.IGUAL_IGUAL):
            if(self.condicion.validarRegla4()):
                optimizacion.regla = "Regla 4"
                optimizacion.despues = "goto "+self.etiqueta+";"
                ReporteOptimizacion.func(optimizacion)
                codigoAugus = "goto "+self.etiqueta+";\n"
            elif(self.condicion.validarRegla5()):
                optimizacion.regla = "Regla 5"
                optimizacion.despues = ""
                ReporteOptimizacion.func(optimizacion)


                #Regla 19 Código Parcialmente Muerto
                etiqueta = ast.obtenerEtiqueta(self.etiqueta)
                etiqueta.ast = ast
                codigoAugus="<div>"+etiqueta.optmimizarCodigo(ast)+"</div>"
                optimizacion = Optimizacion()
                optimizacion.linea = str(etiqueta.linea)
                optimizacion.antes = codigoAugus
                optimizacion.tipo = "Bloques - Eliminación de Código Parcialmente Muerto"
                optimizacion.regla = "Regla 19"
                optimizacion.despues = ""
                ReporteOptimizacion.func(optimizacion)
                ast.etiquetasBetadas.append(etiqueta.id)
                return ""


        #validacion de regla 6 o 7 Mirilla
        optimizacion = Optimizacion()
        optimizacion.linea = str(self.linea)
        optimizacion.antes = codigoAugus
        optimizacion.tipo = "Mirilla - Optimizaciones de flujo de control"
        if(codigoAugus.startswith('goto')):
            optimizacion.regla = "Regla 6"
        else:
            optimizacion.regla = "Regla 7"
        try:
            etiqueta = ast.obtenerEtiqueta(self.etiqueta)
            if(len(etiqueta.instrucciones)>0):
                if isinstance(etiqueta.instrucciones[0],GoTo):
                    if(codigoAugus.startswith('goto')):
                        codigoAugus = "goto "+etiqueta.instrucciones[0].id+";\n"
                    else:
                        codigoAugus = "if( "+self.condicion.generarAugus()+" ) goto "+etiqueta.instrucciones[0].id+";\n"
                        self.etiqueta = etiqueta.instrucciones[0].id
                    optimizacion.despues = codigoAugus
                    ReporteOptimizacion.func(optimizacion)
        except:
            pass
        

       #validacion de regla 3
        try:
            if(codigoAugus.startswith('if')):
                if(len(self.instrucciones)>0):
                    if isinstance(self.instrucciones[0],GoTo):  #validamos que la siguiente instrucción sea un goto
                        condicionNueva = self.condicion.invertirCondicion()
                        
                        if condicionNueva != self.condicion.generarAugus(): #si la condicion si cambio se hace la optimizacion
                            etiquetaFalse = self.instrucciones[0]
                            etiquetaTrue = ast.obtenerEtiqueta(self.etiqueta)

                            codigoOptimizar="<div>"
                            codigoOptimizar+="<p>"+codigoAugus+"</p>"
                            codigoOptimizar+="<p>goto "+etiquetaFalse.id+"</p>"
                            codigoOptimizar+="<p>"+etiquetaTrue.id+":</p>"
                            codigoOptimizar+="<p>[instrucciones]</p>"
                            codigoOptimizar+="<p>"+etiquetaFalse.id+":</p>"
                            codigoOptimizar+="</div>"


                            codigoAugus = "if( "+condicionNueva+" ) goto "+etiquetaFalse.id+";\n"
                            codigoOptimizado="<div>"
                            codigoOptimizado+="<p>"+codigoAugus+"</p>"
                            codigoOptimizado+="<p>[instrucciones]</p>"
                            codigoOptimizado+="<p>"+etiquetaFalse.id+":</p>"
                            codigoOptimizado+="</div>"

                            optimizacion.antes = codigoOptimizar
                            optimizacion.despues =codigoOptimizado
                            optimizacion.regla = "Regla 3"
                            optimizacion.tipo = "Mirilla - Eliminación de Código Inalcanzable"
                            ReporteOptimizacion.func(optimizacion)
                            etiquetaTrue.imprimirEtiqueta = False
                            etiquetaTrue.ast = ast
                            codigoAugus+=etiquetaTrue.optmimizarCodigo(ast)
                            
                            ast.etiquetasBetadas.append(etiquetaTrue.id)

        except:
            pass


        return codigoAugus
        