from ast.Instruccion import Instruccion
from Reporteria.Error import Error 
import Reporteria.ReporteErrores as ReporteErrores
from ast.Simbolo import TIPO_DATO as Tipo  
from ValorImplicito.Operacion import Operacion 
from ValorImplicito.Primitivo import Primitivo 
from ValorImplicito.Operacion import TIPO_OPERACION as Op       
import ast.Temporales as Temp

class Imprimir(Instruccion) :
    def __init__(self,cad,expresiones,linea,columna):
        self.cad = cad
        self.expresiones = expresiones
        self.linea = linea
        self.columna = columna

    def traducir(self,ent,arbol,ventana):
        valorfinal = "print(\""
        cadena = self.cad.traducir(ent,arbol)
        if(cadena == None): return None
        
        if(self.expresiones==None):
            valorfinal += cadena.temporal.utilizar()+"\");"
        else:
            cadena = cadena.temporal.utilizar()
            temporalGenerado = None
            for expresion in self.expresiones:
                exp_3D = expresion.traducir(ent,arbol)
                if(exp_3D == None): return None
                if(expresion.tipo == Op.PRIMITIVO):
                    if(exp_3D.codigo3D != ""):  ventana.consola.appendPlainText(exp_3D.codigo3D) 
                    pos = cadena.index("%")
                    if(pos==-1):
                        error = Error("SEMANTICO","Error semantico, La expresión es incorrecta para imprimir.",self.linea,self.columna)
                        ReporteErrores.func(error)
                        return None
                
                    llave = cadena[pos:pos+2]
                    cadena = self.concatenar(cadena,llave,exp_3D.temporal.utilizar())
                    if(cadena == None): return None 
                
                else:
                    if(exp_3D.codigo3D != ""):  ventana.consola.appendPlainText(exp_3D.codigo3D) 
                    pos = cadena.index("%")
                    if(pos==-1):
                        error = Error("SEMANTICO","Error semantico, La expresión es incorrecta para imprimir.",self.linea,self.columna)
                        ReporteErrores.func(error)
                        return None

                    
                    opIzquierdo = Operacion()
                    opIzquierdo.Primitivo(Primitivo("\""+cadena[0:pos]+"\"",self.linea,self.columna))

                    op = Operacion()
                    op.Operacion(opIzquierdo,expresion,Op.SUMA,self.linea,self.columna)
                    resultOp = op.traducir(ent,arbol)

                    if(resultOp.codigo3D!=""): ventana.consola.appendPlainText(resultOp.codigo3D) 
                    cadena = cadena[pos+2:]

                    if(temporalGenerado==None):
                        temporalGenerado = resultOp.temporal 
                    else:
                        varTemp = resultOp.temporal.obtener()
                        ventana.consola.appendPlainText(varTemp+"="+temporalGenerado.utilizar()+"+"+varTemp+";")
                        temporalGenerado = resultOp.temporal
                    

            if(temporalGenerado == None):
                valorfinal += cadena+"\");"
            else:
               
                temporal = Temp.nuevoTemporal()
                op = temporal.obtener() + '='+temporalGenerado.utilizar()+"+\""+cadena+"\";"
                ventana.consola.appendPlainText(op)
                valorfinal = "print("+temporal.obtener() +");"

        ventana.consola.appendPlainText(valorfinal) 




    def concatenar(self,cadena, llave, valor):

        pos = cadena.index("%")
        pos2 = cadena.index(llave)
        if (pos == -1 or pos2 == -1):
            error = Error("SEMANTICO","Error semantico, La expresión es incorrecta para imprimir.",self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        
        if (pos == pos2):
            cadena = cadena.replace(llave, valor,1)
        else:
            error = Error("SEMANTICO","Error semantico, La expresión es incorrecta para imprimir.",self.linea,self.columna)
            ReporteErrores.func(error)
            return None
        
        return cadena
    