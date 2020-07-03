from Optimizador.OptimizadorAST.Instruccion import Instruccion
from Optimizador.OptimizadorAST.GoTo import GoTo
from Optimizador.OptimizadorCondicionales.If import If
from Optimizador.OptimizadorValorImplicito.Asignacion import Asignacion
from Optimizador.OptimizadorReporteria.Optimizacion import Optimizacion 
import Optimizador.OptimizadorReporteria.ReporteOptimizacion as ReporteOptimizacion

class Etiqueta(Instruccion):
    def __init__(self,  id, instrucciones, linea, columna):
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
        self.codigoOptimizado = ""
        self.imprimirEtiqueta = True

    def optmimizarCodigo(self,ast):
                self.codigoOptimizado = ""
                if(self.imprimirEtiqueta):
                    self.codigoOptimizado += self.id+":\n"

                contador = 0
                instruccionAnterior = None
                asignacionPrevia = None
                codigoAnterior = ""
                for ins in self.instrucciones:
                    # try:
                        if(isinstance(ins,Asignacion)):
                            ins.instruccionPrevia = asignacionPrevia
                            asignacionPrevia = ins
                        elif(isinstance(ins,GoTo)):
                            ins.ast = ast
                        elif(isinstance(ins,If)):
                            ins.instrucciones = self.instrucciones[contador+1:]

                        optimizado = ""
                        if(isinstance(ins,If)): 
                            optimizado = ins.optmimizarCodigo(ast).codigo
                            if(len(ReporteOptimizacion.func(None))>0):
                                if(ReporteOptimizacion.func(None)[-1].regla=="Regla 19"):
                                    if(len(self.instrucciones[contador+1:]) == 0): continue  #si no existen mas instrucciones no hay optimización
                                    optimizacion = Optimizacion() #si hay optimización
                                    optimizacion.linea = str(ins.linea)
                                    codigoOptimizar="<div>"
                                    for i in self.instrucciones[contador+1:]:
                                        if(isinstance(i,GoTo)):
                                            i.ast = ast
                                        elif(isinstance(ins,If)):
                                            continue
                                        codigoOptimizar+="<p>"+i.optmimizarCodigo().codigo+"</p>"
                                    codigoOptimizar+="</div>"
                                    optimizacion.antes = codigoOptimizar
                                    optimizacion.despues = ""
                                    optimizacion.regla = "Regla 20"
                                    optimizacion.tipo = "Bloques - Eliminación de Código Muerto"
                                    ReporteOptimizacion.func(optimizacion)
                                    codigoAnterior = ''
                                    break    
                        else:
                            optimizado = ins.optmimizarCodigo().codigo
                        #Regla 2 Mirilla
                        if(isinstance(ins,GoTo)):
                            if(codigoAnterior.startswith('goto')):
                                if(isinstance(instruccionAnterior,If)):
                                    codigoAnterior = ""
                                    continue
                                else:
                                    optimizacion = Optimizacion() #si hay optimización
                                    optimizacion.linea = str(ins.linea)
                                    optimizacion.antes = codigoOptimizar
                                    optimizacion.despues = ""
                                    optimizacion.regla = "Regla 20"
                                    optimizacion.tipo = "Bloques - Eliminación de Código Muerto"
                                    ReporteOptimizacion.func(optimizacion)
                                    codigoAnterior = ''
                            elif(ast.existeEtiqueta(ins.id)):
                                if(optimizado!=""):
                                    self.codigoOptimizado += "    "+optimizado
                                    codigoAnterior = optimizado
                                if(len(self.instrucciones[contador+1:]) == 0): continue  #si no existen mas instrucciones no hay optimización
                                optimizacion = Optimizacion() #si hay optimización
                                optimizacion.linea = str(ins.linea)
                                codigoOptimizar="<div>"
                                for i in self.instrucciones[contador+1:]:
                                    if(isinstance(i,GoTo)):
                                        i.ast = ast
                                    elif(isinstance(ins,If)):
                                        continue
                                    codigoOptimizar+="<p>"+i.optmimizarCodigo().codigo+"</p>"
                                codigoOptimizar+="</div>"
                                optimizacion.antes = codigoOptimizar
                                optimizacion.despues = ins.id+":"
                                optimizacion.regla = "Regla 2"
                                optimizacion.tipo = "Mirilla - Eliminación de Código Inalcanzable"
                                ReporteOptimizacion.func(optimizacion)
                                codigoAnterior = ''
                                break
                            else:
                                if(optimizado!=""):
                                    self.codigoOptimizado += "    "+optimizado
                                    codigoAnterior = optimizado
                        else:
                            if(optimizado!=""):
                                self.codigoOptimizado += "    "+optimizado
                                codigoAnterior = optimizado

                        instruccionAnterior = ins
                        contador = contador + 1
                    # except:
                    #    pass
                return self.codigoOptimizado
    def generarAugus(self):
        pass