class Entorno:
    def __init__(self,anterior):
        self.tabla = {}
        self.anterior = anterior
        self.consola = None

    def asignarConsola(self,consola):
        self.consola = consola

    def agregar(self, simbolo) :
        self.tabla[simbolo.id] = simbolo

    def obtenerLocal(self, id) :
        id = id
        if not id in self.tabla :
            return None

        return self.tabla[id]

    def existe(self,id):
        id = id
        return self.obtenerLocal(id)

    def obtener(self,id):
        return self.obtenerLocal(id)
            
    def eliminar(self,id):
        id = id
        if(self.obtenerLocal(id) != None):
            del self.tabla[id]

    def reemplazar(self,simbolo):
        simbolo.id = simbolo.id
        if(self.obtenerLocal(simbolo.id) != None):
            self.tabla[simbolo.id] = simbolo