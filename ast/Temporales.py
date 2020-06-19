class Temporal():
    def __init__(self,nombre):
        self.nombre = nombre
        self.utilizado = False

    def obtener(self):
        return self.nombre

    def utilizar(self):
        self.utilizado = True
        return self.nombre

class Resultado3D():
    def __init__(self):
        self.codigo3D = ""
        self.temporal = None
        self.tipo = None
        self.trueLabels = []
        self.falseLabels = []
        self.ifSalidaLabel = ""


def temporal(reset = False):
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(temporal,"contador"):
        temporal.contador = 0
        return "$t0"

    if(reset):
        temporal.contador = 0
    else:
        temporal.contador = temporal.contador + 1
        return "$t"+str(temporal.contador)