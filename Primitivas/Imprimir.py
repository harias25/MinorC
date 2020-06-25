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
        cadena = self.cad.traducir(ent,arbol,ventana)
        if(cadena == None): return None
        
        if(self.expresiones==None):
            if(cadena.tipo == Tipo.CHAR):
                valorfinal = "print("+cadena.temporal.utilizar()+");"
            else:
                valorfinal += cadena.temporal.utilizar()+"\");"      
        else:
            cadena = cadena.temporal.utilizar()
            cadena = cadena[1:-1]
            for expresion in self.expresiones:
                exp_3D = expresion.traducir(ent,arbol,ventana)
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

                  

                    ventana.consola.appendPlainText("print(\""+cadena[0:pos]+"\");") 
                    if(exp_3D.codigo3D != ""):  ventana.consola.appendPlainText(exp_3D.codigo3D) 
                    
                    ventana.consola.appendPlainText("print("+exp_3D.temporal.utilizar()+");") 
                    cadena = cadena[pos+2:]

            valorfinal += cadena+"\");"

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
    