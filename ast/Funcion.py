from ast.Instruccion import Instruccion
from ValorImplicito.Asignacion import Asignacion
import ast.Entorno as TS
import ValorImplicito.Asignacion as Asignacion
import ast.Temporales as temp
from ValorImplicito.LlamadaFuncion import LlamadaFuncion
from Transferencia.Return import Return

class Funcion(Instruccion) :
    def __init__(self, tipo, id, instrucciones,parametros,linea,columna) :
        self.tipo = tipo
        self.id = id
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
        self.parametros = parametros
        self.temporales = []
        self.entorno = None
        self.etiqueta = None
        self.nivelesRecursiva = 0

    def inicializar(self,ent,arbol,ventana):
        self.entorno = TS.Entorno(ent)
        self.temporales = []    
        for parametro in self.parametros:
            temporal = parametro.traducir(self.entorno,arbol,ventana)
            if(temporal != None): self.temporales.append(temporal)

        
        #self.calcularNiveles(self.instrucciones)



    def calcularNivelesValor(self,ins):
        try:
            if(isinstance(ins.operadorIzq,LlamadaFuncion)):
                if(ins.operadorIzq.id == self.id):
                    self.nivelesRecursiva = self.nivelesRecursiva  + 1
            elif(ins.operadorIzq != None):
                self.calcularNivelesValor(ins.operadorIzq)

            if(isinstance(ins.operadorDer,LlamadaFuncion)):
                if(ins.operadorDer.id == self.id):
                    self.nivelesRecursiva = self.nivelesRecursiva  + 1

            elif(ins.operadorDer != None):
                self.calcularNivelesValor(ins.operadorDer)

            if(isinstance(ins,Return)):
                self.calcularNivelesValor(ins.valor)

        except:
            pass


    def calcularNiveles(self,instrucciones):
        for ins in instrucciones:
            try:
                if(isinstance(ins,LlamadaFuncion)):
                    if(ins.id == self.id):
                        self.nivelesRecursiva = self.nivelesRecursiva  + 1
                else:
                    if("instrucciones" in ins.__dict__):
                        self.calcularNiveles(ins.instrucciones)

                    if("instruccionesV" in ins.__dict__):
                        self.calcularNiveles(ins.instruccionesV)

                    if("instruccionesF" in ins.__dict__):
                        self.calcularNiveles(ins.instruccionesF)

                    if("listaElseIF" in ins.__dict__):
                        self.calcularNiveles(ins.listaElseIF)

                    if("lista_case" in ins.__dict__):
                        self.calcularNiveles(ins.lista_case)

                    if("valor" in ins.__dict__):
                        self.calcularNivelesValor(ins.valor)
                    
            except:
                pass
        
    def traducir(self,ent,arbol,ventana):
        
        ventana.editor.append("\n"+self.etiqueta+":"+"#"+self.id)
        for ins in self.instrucciones:
            try:
                ins.traducir(self.entorno,arbol,ventana)
            except:
                pass

        

    def getTipo(self):
        return self.tipo.name