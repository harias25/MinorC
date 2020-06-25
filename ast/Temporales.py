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

def listaContinue(tipo,valor):
    if not hasattr(listaContinue,"lista"):
        listaContinue.lista = []

    if(tipo==0): #se agrega
        listaContinue.lista.append(valor)
    elif(tipo==1):
        if(len(listaContinue.lista)>0):
            return listaContinue.lista[-1]
    elif(tipo==2):
        if(len(listaContinue.lista)>0):
            listaContinue.lista.remove(valor)
    elif(tipo==-1):
        listaContinue.lista = []

def listaBreak(tipo,valor):
    if not hasattr(listaBreak,"lista"):
        listaBreak.lista = []

    if(tipo==0): #se agrega
        listaBreak.lista.append(valor)
    elif(tipo==1):
        if(len(listaBreak.lista)>0):
            return listaBreak.lista[-1]
    elif(tipo==2):
        if(len(listaBreak.lista)>0):
            listaBreak.lista.remove(valor)
    elif(tipo==-1):
        listaBreak.lista = []
    

def listaReturn(tipo,valor):
    if not hasattr(listaReturn,"lista"):
        listaReturn.lista = []

    if(tipo==0): #se agrega
        listaReturn.lista.append(valor)
    elif(tipo==1):
        if(len(listaReturn.lista)>0):
            return listaReturn.lista[0]
    elif(tipo==2):
        if(len(listaReturn.lista)>0):
            listaReturn.lista.remove(valor)
    elif(tipo==-1):
        listaReturn.lista = []

def listaLLamada(tipo,valor):
    if not hasattr(listaLLamada,"lista"):
        listaLLamada.lista = []

    if(tipo==0): #se agrega
        listaLLamada.lista.append(valor)
    elif(tipo==1):
        if(len(listaLLamada.lista)>0):
            return listaLLamada.lista[0]
    elif(tipo==2):
        if(len(listaLLamada.lista)>0):
            listaLLamada.lista.remove(valor)
    elif(tipo==-1):
        listaLLamada.lista = []

def listaRecusion(tipo,valor):
    if not hasattr(listaRecusion,"lista"):
        listaRecusion.lista = []

    if(tipo==0): #se agrega
        listaRecusion.lista.append(valor)
    elif(tipo==1):
        if(len(listaRecusion.lista)>0):
            return listaRecusion.lista[0]
    elif(tipo==2):
        if(len(listaRecusion.lista)>0):
            listaRecusion.lista.remove(valor)
    elif(tipo==-1):
        listaRecusion.lista = []
    