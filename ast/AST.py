from ast.Entorno import Entorno

class AST:
    def __init__(self,instrucciones):
        self.instrucciones = instrucciones
        self.etiquetas = []
        self.structs = []
        self.entornoGlobal = Entorno(None)

    def existeEtiqueta(self,id):
        for etiqueta in self.etiquetas:
            comparacion = etiqueta.id == id.id
            if(comparacion):
                return True

        return False
    
    def agregarEtiqueta(self,etiqueta):
        self.etiquetas.append(etiqueta)

    def obtenerStruct(self,texto):
        for struct in self.structs:
            if(struct.id == texto):
                return struct

        return None


    def existeStruct(self,id):
        for struct in self.structs:
            comparacion = struct.id == id.id
            if(comparacion):
                return True

        return False
    
    def agregarStruct(self,struct):
        self.structs.append(struct)

    def obtenerEtiqueta(self,texto):
        for etiqueta in self.etiquetas:
            if(etiqueta.id == texto):
                return etiqueta

        return None

    def reemplazarEtiqueta(self,funcion):
        contador = 0
        for etiqueta in self.etiquetas:
            if(etiqueta.id == funcion.id):
                self.etiquetas[0] = funcion
                break
            contador = contador + 1


    def obtenerSiguienteEtiqueta(self,texto):
        contador = 0
        for etiqueta in self.etiquetas:
            if(etiqueta.id == texto):
                if(len(self.etiquetas) > (contador+1)):
                 return self.etiquetas[contador+1]
            contador = contador +1

        return None