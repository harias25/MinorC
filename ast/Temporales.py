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


def nuevoTemporal(op = 1):
    if not hasattr(nuevoTemporal,"lista"):
        nuevoTemporal.lista = []
    if(op==0):
        nuevoTemporal.lista = []
    elif(op==1):
        temp = Temporal(temporal())
        nuevoTemporal.lista.append(temp)
        return temp


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

def parametro(reset = False):
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(parametro,"contador"):
        parametro.contador = 0
        return "$a0"

    if(reset):
        parametro.contador = 0
    else:
        parametro.contador = parametro.contador + 1
        return "$a"+str(parametro.contador)

def etiqueta(reset = False):
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(etiqueta,"contador"):
        etiqueta.contador = 0
        return "L0"

    if(reset):
        etiqueta.contador = 0
    else:
        etiqueta.contador = etiqueta.contador + 1
        return "L"+str(etiqueta.contador)