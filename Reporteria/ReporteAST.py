import os
import ast
import ValorImplicito as V
from ValorImplicito.AccesoStruct import AccesoStruct
from ply.lex import LexToken
import webbrowser

class ReporteAST():
    def __init__(self):
        self.contador = 0
        self.contenido = ""

    def graficar(self,instrucciones):
        pagina = "<html>" + '\n' + "<head>" + '\n' + "<title>Reporte de Simbolos</title>" + '\n' + "</head>" + '\n'
        pagina = pagina + "<body bgcolor=\"black\">" + '\n' + "<center><Font size=22 color=darkred>" + "Reporte AST" + "</Font></center>" + '\n'
        pagina = pagina + "<hr >" + '\n' + "<font color=white>" + '\n' + "<center>" + '\n'

        self.contenido = "digraph G {\n"
        self.contenido += "node [style=filled];\n"
        self.contenido += "S->glo [color=\"0.002 0.782 0.999\"];\n"
        self.contenido += ""
        self.contenido += ""

        for nodo in instrucciones:
            self.definirEtiquetas(nodo,"ni")

        self.contenido += "S [color=\"0.449 0.447 1.000\"];\n"
        self.contenido += "glo [color=\"0.423 0.133 1.000\", label=\"Globales\"];\n"
        self.contenido += "ni [color=\"0.201 0.753 1.000\", label=\"Funciones\"];\n"
        self.contenido += "glo->ni [color=\"0.002 0.782 0.999\"];\n"
        self.contenido += "}"

        f = open ('AST.dot','w')
        f.write(self.contenido)
        f.close()

        os.system("dot -Tpng AST.dot -o AST.png")
        os.system("DEL /F /A AST.dot")

        pagina = pagina +' <img src="AST.png" alt="AST GENERADO"> '

        pagina = pagina + '\n' + "</center>" + '\n' + "</table>" + "</body>" + '\n' + "</html>"

        f = open ('reporteAST.html','w')
        f.write(pagina)
        f.close()
        webbrowser.open_new_tab('reporteAST.html')

    def definirEtiquetas(self,nodo,padre):
        try:
            if (isinstance(nodo,ast.Funcion.Funcion)):
                self.contador=self.contador+1
                self.contenido += "node" + str(self.contador) + "[label = \"" + nodo.getTipo()+":"+nodo.id+ "\", style = filled, color = lightblue];\n"
                self.contenido += padre+"->"+"node" + str(self.contador) +";\n"
                padre = "node" + str(self.contador)
                for hijo in nodo.instrucciones:
                    if(not isinstance(hijo,LexToken)):
                        self.definirInstrucciones(hijo,padre)
            else:
                self.definirInstrucciones(nodo,"glo")

        except:
            pass

    def definirInstrucciones(self,nodo,padre):
        try:
            self.contador=self.contador+1
            padreI = "node" + str(self.contador)
            if(isinstance(nodo,V.Asignacion.Asignacion)):
                self.contenido += padreI + "[label = \"" + "Asignacion" + "\", style = filled, color = darkturquoise];\n"
            else:
                self.contenido += padreI + "[label = \"" + type(nodo).__name__ + "\", style = filled, color = darkturquoise];\n"
            self.contenido += padre+"->"+padreI+";\n"
            for key in nodo.__dict__:
                if(key!="linea" and key!="columna" and key!="declarada"  and key!="puntero" and key!="defArray"):
                    if(isinstance(nodo.__dict__[key],V.Operacion.Operacion)):
                        if(isinstance(nodo,V.Asignacion.Asignacion)):
                            self.contador=self.contador+1
                            self.contenido += "node" + str(self.contador) + "[label = \"" + "=" + "\", style = filled, color = darkturquoise];\n"
                            self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        self.definirExpresion(nodo.__dict__[key],padreI,"Expresion")
                    
                    elif key=="expresiones":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "expresiones" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirExpresion(llave,top,"Expresion")

                    elif key=="declaraciones":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Declaraciones" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)

                    elif key=="instruccionesV":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "InstruccionesVerdadero" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)

                    elif key=="instruccionesF":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "InstruccionesElse" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)

                    elif key=="listaElseIF":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "ListaElseIf" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)

                    elif key=="lista_case":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "ListaCase" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)

                    elif key=="default":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Defualt" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        self.definirInstrucciones(nodo.__dict__[key],top)

                    elif key=="instruccion":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Instruccion" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        self.definirInstrucciones(nodo.__dict__[key],top)

                    elif key=="operacion":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Operacion" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        self.definirInstrucciones(nodo.__dict__[key],top)

                    elif key=="llave" and isinstance(nodo.__dict__[key],V.AccesoLista.AccesoLista):
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Llave" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        self.definirInstrucciones(nodo.__dict__[key],top)

                    elif key=="id" and isinstance(nodo.__dict__[key],V.AccesoLista.AccesoLista):
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Id" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        self.definirInstrucciones(nodo.__dict__[key],top)


                    elif key=="case":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Case" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)

                    elif key=="instrucciones":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Instrucciones" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirInstrucciones(llave,top)
                    
                    elif key=="lista":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "ListaDeclaracion" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            if(isinstance(llave,list)):
                                for subllave in llave:
                                    self.definirInstrucciones(subllave,top)
                            elif(isinstance(llave,str)):
                                self.contador=self.contador+1
                                self.contenido += "node" + str(self.contador) + "[label = \"" + llave + "\", style = filled, color = darksalmon];\n"
                                self.contenido += top+"->"+"node" + str(self.contador) +";\n"
                            else:
                                self.definirInstrucciones(llave,top)

                    elif key=="llaves":
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "llaves" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirExpresion(llave,top,"Expresion")
                    elif(key=="valor" and isinstance(nodo.__dict__[key],list)):
                        self.contador=self.contador+1
                        self.contenido += "node" + str(self.contador) + "[label = \"" + "Valores" + "\", style = filled, color = gold1];\n"
                        self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        top = "node" + str(self.contador) 
                        for llave in nodo.__dict__[key]:
                            self.definirExpresion(llave,top,"Expresion")
                    else:
                        self.contador=self.contador+1
                        sub_nodo = nodo.__dict__[key]
                        if(sub_nodo!=None):
                            if(isinstance(sub_nodo,AccesoStruct)):
                                self.contenido += "node" + str(self.contador) + "[label = \"" + "Id" + "\", style = filled, color = gold1];\n"
                                self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                                top = "node" + str(self.contador) 
                                self.definirInstrucciones(nodo.__dict__[key],top)
                            else:
                                self.contenido += "node" + str(self.contador) + "[label = \"" + str(key)+":"+str(nodo.__dict__[key]) + "\", style = filled, color = darkseagreen3];\n"
                                self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
        except:
            pass

    def definirExpresion(self,nodo,padre,label):
        self.contador=self.contador+1
        self.contenido += "node" + str(self.contador) + "[label = \"" + label + "\", style = filled, color = darkseagreen3];\n"
        self.contenido += padre+"->"+"node" + str(self.contador) +";\n"
        padreI = "node" + str(self.contador)
        for key in nodo.__dict__:
            if(key!="linea" and key!="columna" and nodo.__dict__[key] != None):
                if(isinstance(nodo.__dict__[key],V.Primitivo.Primitivo)):
                    self.definirExpresion(nodo.__dict__[key],padreI,"Primitivo") 
                elif(key=="valor" and isinstance(nodo.__dict__[key],dict)):
                    self.contador=self.contador+1
                    self.contenido += "node" + str(self.contador) + "[label = \"" + "=" + "\", style = filled, color = darkturquoise];\n"
                    self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                    self.contador=self.contador+1
                    self.contenido += "node" + str(self.contador) + "[label = \"" + "Array()" + "\", style = filled, color = darksalmon];\n"
                    self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                elif(key=="tipo" and nodo.__dict__[key]):
                    self.contador=self.contador+1
                    self.contenido += "node" + str(self.contador) + "[label = \"" + str(key)+":"+str(nodo.__dict__[key].name) + "\", style = filled, color = darksalmon];\n"
                    self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                elif(isinstance(nodo.__dict__[key],V.Operacion.Operacion)):
                        if(isinstance(nodo,V.Asignacion.Asignacion)):
                            self.contador=self.contador+1
                            self.contenido += "node" + str(self.contador) + "[label = \"" + "=" + "\", style = filled, color = darkturquoise];\n"
                            self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                        self.definirExpresion(nodo.__dict__[key],padreI,key)
                elif(isinstance(nodo.__dict__[key],AccesoStruct)):
                    self.contador=self.contador+1
                    self.contenido += "node" + str(self.contador) + "[label = \"AccesoStruct\", style = filled, color = darksalmon];\n"
                    self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                    top = "node" + str(self.contador) 
                    self.definirExpresion(nodo.__dict__[key],top,"AccesoStruct")
                elif(isinstance(nodo.__dict__[key],V.AccesoLista.AccesoLista)):
                    self.contador=self.contador+1
                    self.contenido += "node" + str(self.contador) + "[label = \"Valor\", style = filled, color = darksalmon];\n"
                    self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                    top = "node" + str(self.contador) 
                    self.definirInstrucciones(nodo.__dict__[key],top)
                else:
                    self.contador=self.contador+1
                    self.contenido += "node" + str(self.contador) + "[label = \"" + str(key)+":"+str(nodo.__dict__[key]) + "\", style = filled, color = darksalmon];\n"
                    self.contenido += padreI+"->"+"node" + str(self.contador) +";\n"
                
            