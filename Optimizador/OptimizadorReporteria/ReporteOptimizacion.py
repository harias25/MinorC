import webbrowser

def func(opt,param=False):
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(func,"listado"):
        func.listado = []

    if(param):
        func.listado = []
    else:
        if(opt!=None):
            func.listado.append(opt)
        else:
            return func.listado

class ReporteOptimizacion():
    def ReporteOptimizacion(self):
        listado = func(None)


        contenido = "<html>" + '\n' + "<head>" + '\n' + "<title>Reporte de Optimización</title>" + '\n' + "</head>" + '\n'
        contenido = contenido + "<body bgcolor=\"black\">" + '\n' + "<center><Font size=22 color=darkred>" + "Reporte de Optimización Augus" + "</Font></center>" + '\n'
        contenido = contenido + "<hr >" + '\n' + "<font color=white>" + '\n' + "<center>" + '\n'
        contenido = contenido + "<table border=1 align=center style=\"width:100%;\" >" + '\n'
        contenido = contenido + "<TR bgcolor=darkred>" + "\n"
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>No.</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:25%; color:white\" align=center>Tipo de Regla</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:15%; color:white\" align=center>Regla</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:20%; color:white\" align=center>Antes</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:20%; color:white\" align=center>Despues</TH>" + '\n'
        contenido = contenido + "<TH  style=\"font-size: 18px; width:10%; color:white\" align=center>Linea</TH>" + '\n'
        contenido = contenido + "</TR>" + '\n'



        if(listado == None): listado = []
        cont = 0
        for opt in listado:
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" align=center>" + str(cont) + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + opt.tipo + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + opt.regla + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + opt.antes + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + opt.despues + "</TD>" + '\n'
            contenido = contenido + "<TD style=\"font-size: 15px; color:white;\" color:white align=center>" + opt.linea + "</TD>" + '\n'
            contenido = contenido + "</TR>" + '\n'
            cont = cont + 1

        contenido = contenido + '\n' + "</center>" + '\n' + "</table>" + "</body>" + '\n' + "</html>"

        f = open ('reporteOptimizacion.html','w')
        f.write(contenido)
        f.close()

        webbrowser.open_new_tab('reporteOptimizacion.html')
        