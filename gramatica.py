from ast.Instruccion import Instruccion
from ast.Declaracion import Declaracion
from ast.Parametro import Parametro
from ast.Funcion import Funcion
from ast.Simbolo import TIPO_DATO as Tipo
from ValorImplicito.Operacion import Operacion
from ValorImplicito.Asignacion import Asignacion
from ValorImplicito.Operacion import TIPO_OPERACION
from ValorImplicito.Primitivo import Primitivo
from  Primitivas.Imprimir import Imprimir
from  Primitivas.Scan import Scan
import ply.yacc as yacc
import Reporteria.Error as Error
import Reporteria.ValorAscendente as G
import Reporteria.ReporteErrores as ReporteErrores
from Condicionales.If import If
from Condicionales.Switch import Switch
from Condicionales.While import While
from Condicionales.For import For
from Condicionales.DoWhile import DoWhile
from Condicionales.Case import Case
from Transferencia.Break import Break

reservadas = {
    'int'	: 'INT',
    'float' : 'FLOAT',
    'char'	: 'CHAR',
    'printf' : 'IMPRIMIR',
	'xor'	: 'XOR',
    'void'  : 'VOID',
    'if'    : 'IF',
    'else'  : 'ELSE',
    'switch': 'SWITCH',
    'case'  : 'CASE',
    'default' : 'DEFAULT',
    'break' : 'BREAK',
    'scanf' : 'SCAN',
    'do'    : 'DO',
    'while' : 'WHILE',
    'for'   : 'FOR',
}

tokens  = [
    'PTCOMA',
	'DOSP',
    'PARIZQ',
    'PARDER',
    'LLAVIZQ',
    'LLAVDER',
	'CORIZQ',
    'CORDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'RESTO',
    'MENQUE',
    'MAYQUE',
    'MEIQUE',
    'MAIQUE',
    'IGUALQUE',
    'NIGUALQUE',
	'AND',
    'OR',
	'NOTR',
    'NOT',
	'XORR',
	'SHIFTI',
	'SHIFTD',
    'ID',
	'DECIMAL',
    'ENTERO',
    'CADENA',
    'CADENAR_CHAR',
    'PAND',
    'BOR',
    'PUNTO',
    'FLECHA',
    'COMA',
    'MULTIPLICATIVA',
    'DIVIDIDA',
    'ARESTO',
    'ASUMA',
    'ARESTA',
    'ASHIFTI',
    'ASHIFTD',
    'APAND',
    'AXORR',
    'ABOR',
    'UNARIO'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_DOSP		= r':'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_RESTO     = r'%'

t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_MEIQUE    = r'<='
t_MAIQUE    = r'>='
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='

t_PAND       = r'&'
t_BOR       = r'\|'

t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOTR		= r'~'
t_NOT       = r'!'
t_XORR       = r'\^'

t_SHIFTI    = r'<<'
t_SHIFTD    = r'>>'

t_PUNTO     = r'.'
t_COMA     = r'\,'
t_FLECHA    = r'->'


t_ARESTA = r'-='
t_ASUMA = r'\+='
t_MULTIPLICATIVA = r'\*='
t_DIVIDIDA = r'/='
t_ARESTO = r'%='
t_ASHIFTI = r'<<='
t_ASHIFTD = r'>>='
t_APAND = r'&='
t_AXORR = r'\^='
t_ABOR = r'\|='
t_UNARIO = r'\?:'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')    # Check for reserved words
     return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_CADENAR_CHAR(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
     r'\n+'
     t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    error = Error.Error("LEXICO","Error lexico, Caracter "+t.value[0]+" no es valido.",t.lexer.lineno,find_column(t))
    ReporteErrores.func(error)
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

textoEntrada = ""
# Funcion para obtener la columna
def find_column(token):
    line_start = textoEntrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    #('left','CONCAT'),
    ('left','COMA'),
    ('right','IGUAL','MULTIPLICATIVA','DIVIDIDA','ARESTO','ASUMA','ARESTA','ASHIFTD','ASHIFTI','APAND','AXORR','ABOR'),
    ('right','UNARIO'),
    ('left','OR'),
    ('left','AND'),
    ('left','BOR'),
    ('left','XORR'),
    ('left','PAND'),
    ('left','IGUALQUE','NIGUALQUE'),
    ('left','MENQUE','MAYQUE','MEIQUE','MAIQUE'),
    ('left','SHIFTD','SHIFTI'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','RESTO'),
    ('right','UMENOS','NOT','NOTR'),
    ('left','PARIZQ','PARDER','CORIZQ','CORDER','PUNTO','FLECHA'),
    )

#precedence nonassoc menor,mayor, menor_igual,mayor_igual;
def func(tipo,valor):
 
    #Declaración e inicilizacion de la variable "estática"
    if not hasattr(func,"listado"):
        func.listado = []

    if(tipo==0):
        func.listado = []

    if(valor!=None):
        func.listado.append(valor)

    if(tipo==1):
        return func.listado


def p_init(t) :
    'init            : globales'
    t[0] = t[1]

def p_init_empty(t):
    'init            : empty'
    t[0] = t[1]


#********************************************** FUNCIONES  **************************************
def p_etiquetas_lista(t) :
    'globales    : globales iglobal'
    t[1].append(t[2])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('globales -> globales iglobal','globales.lista = globales1.lista; </hr> globales.lista.add(iglobal)',None)
    func(2,gramatical)

def p_etiquetas(t) :
    'globales    : iglobal '
    t[0] = [t[1]]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('globales -> iglobal','globales.lista = [iglobal]',lista)
    func(0,gramatical)

def p_iglobal(t):
    ''' iglobal : funcion 
                | declaracion PTCOMA'''
    t[0] = t[1]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('iglobal -> '+str(t.slice[1]),'iglobal.instr = '+str(t.slice[1])+'.instr;',lista)
    func(0,gramatical)

def p_empty(t) :
    'empty :'
    t[0] = []

def p_funcion_s(t) :
    'funcion    : TIPO ID PARIZQ PARDER LLAVIZQ  instrucciones LLAVDER '
    lista = func(1,None).copy()
    t[0] = Funcion(t[1],t[2],t[6],None,t.slice[2].lineno,find_column(t.slice[2]))
    gramatical = G.ValorAscendente('funcion -> TIPO ID () { instrucciones } ','funcion.instrucciones.lista = []; </hr> funcion.instrucciones.lista = instrucciones.lista; funcion.tipo = TIPO; funcion.id = ID;',lista)
    func(0,gramatical)

def p_f_parametros(t) :
    'funcion    : TIPO ID PARIZQ parametros PARDER LLAVIZQ  instrucciones LLAVDER '
    lista = func(1,None).copy()
    t[0] = Funcion(t[1],t[2],t[7],t[4],t.slice[2].lineno,find_column(t.slice[2]))
    gramatical = G.ValorAscendente('funcion -> TIPO ID () { instrucciones } ','funcion.instrucciones.lista = []; </hr> funcion.instrucciones.lista = instrucciones.lista; funcion.tipo = TIPO; funcion.id = ID;',lista)
    func(0,gramatical)
#*********************************************************** PARAMETROS **********************************************
def p_parametros_lista(t) :
    'parametros    : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('parametros -> parametros COMA parametro','parametros.lista = parametros1.lista; </hr> parametros.lista.add(parametro)',None)
    func(2,gramatical)

def p_parametros(t) :
    'parametros    : parametro '
    t[0] = [t[1]]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('parametros -> parametro','parametros.lista = [parametro]',lista)
    func(0,gramatical)

def p_parametro(t):
    'parametro : TIPO ID'
    t[0] = Parametro(t[1],t[2],t.slice[2].lineno,find_column(t.slice[2]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('parametro -> TIPO ID ','parametro.instr = Declaracion(TIPO,ID);',lista)
    func(0,gramatical)

#********************************************** INSTRUCCIONES  ***********************************

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instrucciones -> instrucciones instruccion','instrucciones.lista = instrucciones1.lista; </hr> instrucciones.lista.add(instruccion);',[])
    func(2,gramatical)#func(0,gramatical)

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instrucciones -> instruccion','instrucciones.lista = [instruccion]',[])
    func(2,gramatical)#func(0,gramatical)

def p_instruccion(t) :
    '''instruccion      : imprimir_instr 
                        | asignacion PTCOMA
                        | declaracion PTCOMA
                        | sentencia_if
                        | sentencia_switch
                        | ins_break
                        | ins_scan
                        | ins_while
                        | ins_for
                        | error   '''

    t[0] = t[1]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instruccion -> '+str(t.slice[1]),'instruccion.instr = '+str(t.slice[1])+'.instr;',lista)
    func(0,gramatical)

#**************************************************** FOR ***************************************************
def p_ins_for(t):
    'ins_for : FOR PARIZQ instruccion_for PTCOMA expresion PTCOMA asignacion PARDER LLAVIZQ instrucciones LLAVDER '
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('ins_for ->FOR PARIZQ instruccion_for PTCOMA expresion PTCOMA expresion_numerica PARDER LLAVIZQ instrucciones LLAVDER ','ins_for.instr = For(instruccion,expresion,expresion_numerica,instrucciones);',lista)
    func(0,gramatical)
    t[0] = For(t[3],t[5],t[7],t[10],t.slice[1].lineno,find_column(t.slice[1]))

def p_instruccion_for(t):
    '''instruccion_for : asignacion 
                       | declaracion '''

    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('instruccion_for -> declaracion | asignacion ','instruccion_for.instr = instruccion;',lista)
    func(0,gramatical)
    t[0] = t[1]

#********************************************* WHILE Y DO WHILE*************************************************
def p_ins_while(t) :
    'ins_while : WHILE PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] = While(t[3],t[6],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('ins_while ->WHILE PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER','ins_while.instr = While(expresion,instrucciones);',lista)
    func(0,gramatical)

def p_ins_do_while(t) :
    'ins_while : DO LLAVIZQ instrucciones LLAVDER WHILE PARIZQ expresion PARDER PTCOMA'
    t[0] = DoWhile(t[7],t[3],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('ins_while ->DO LLAVIZQ instrucciones LLAVDER WHILE PARIZQ expresion PARDER PTCOMA','ins_while.instr = DoWhile(expresion,instrucciones);',lista)
    func(0,gramatical)

#********************************************* SENTENCIA SWITCH ****************************************
def p_sentencia_switch(t):
    'sentencia_switch : SWITCH PARIZQ expresion PARDER LLAVIZQ lista_case default_ins LLAVDER'
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('sentencia_switch ->SWITCH PARIZQ expresion PARDER LLAVIZQ lista_case default LLAVDER','sentencia_switch.instr = Switch(expresion,lista_case,default);',lista)
    func(0,gramatical)
    t[0] = Switch(t[3],t[6],t[7],t.slice[1].lineno,find_column(t.slice[1]))

def p_sentencia_switch_sc(t):
    'sentencia_switch : SWITCH PARIZQ expresion PARDER LLAVIZQ lista_case LLAVDER'
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('sentencia_switch ->SWITCH PARIZQ expresion PARDER LLAVIZQ lista_case LLAVDER','sentencia_switch.instr = Switch(expresion,lista_case,None);',lista)
    func(0,gramatical)
    t[0] = Switch(t[3],t[6],None,t.slice[1].lineno,find_column(t.slice[1]))
def p_lista_case(t):
    'lista_case    : lista_case caso'
    t[1].append(t[2])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('lista_case -> lista_case caso','lista_case.lista = lista_case1.lista; </hr> lista_case.lista.add(caso);',[])
    func(2,gramatical)#func(0,gramatical)

def p_lista_case_s(t) :
    'lista_case    : caso '
    t[0] = [t[1]]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('lista_case -> caso','lista_case.lista = [caso]',[])
    func(2,gramatical)#func(0,gramatical)

def p_caso(t):
    'caso    : CASE expresion DOSP instrucciones  '
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('case ->CASE expresion DOSP instrucciones','case.instr = Case(expresion,instrucciones);',lista)
    func(0,gramatical)
    t[0] = Case(t[2],t[4],t.slice[1].lineno,find_column(t.slice[1]))
def p_caso_S(t):
    'caso    : CASE expresion DOSP  '
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('case ->CASE expresion DOSP','case.instr = Case(expresion,[]);',lista)
    func(0,gramatical)
    t[0] = Case(t[2],[],t.slice[1].lineno,find_column(t.slice[1]))
def p_default(t):
    'default_ins    : DEFAULT DOSP instrucciones  '
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('default_ins ->DEFAULT DOSP instrucciones','default_ins.instr = Case(None,instrucciones);',lista)
    func(0,gramatical)
    t[0] = Case(None,t[3],t.slice[1].lineno,find_column(t.slice[1]))
def p_default_S(t):
    'default_ins    : DEFAULT DOSP  '
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('default_ins ->CASE expresion DOSP','default_ins.instr = Case(None,[]);',lista)
    func(0,gramatical)
    t[0] = Case(None,[],t.slice[1].lineno,find_column(t.slice[1]))
def p_break(t):
    'ins_break : BREAK PTCOMA '
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('ins_break ->BREAK PTCOMA','ins_break.instr = Break();',lista)
    func(0,gramatical)
    t[0] = Break(t.slice[1].lineno,find_column(t.slice[1]))
    
#********************************************* SENTENCIA IF *********************************************
def p_sentencia_if(t):
    'sentencia_if  : IF PARIZQ expresion PARDER LLAVIZQ  instrucciones LLAVDER'
    t[0] = If(t[3],t[6],[],[],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('sentencia_if ->IF PARIZQ expresion PARDER LLAVIZQ  instrucciones LLAVDER','sentencia_if.instr = If(expresion,instruccionesV,[],[]);',lista)
    func(0,gramatical)

def p_sentencia_if_else(t):
    'sentencia_if  : IF PARIZQ expresion PARDER LLAVIZQ  instrucciones LLAVDER ELSE  LLAVIZQ  instrucciones LLAVDER '
    t[0] = If(t[3],t[6],t[10],[],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('sentencia_if ->IF PARIZQ expresion PARDER LLAVIZQ  instrucciones LLAVDER ELSE  LLAVIZQ  instrucciones LLAVDER','sentencia_if.instr = If(expresion,instruccionesV,[],instruccionesF);',lista)
    func(0,gramatical)

def p_sentencia_if_elif_else(t):
    'sentencia_if  : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lelseif ELSE LLAVIZQ instrucciones LLAVDER'
    t[0] = If(t[3],t[6],t[11],t[8],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('sentencia_if ->IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lelseif ELSE LLAVIZQ instrucciones LLAVDER','sentencia_if.instr = If(expresion,instruccionesV,lelseif,instruccionesF);',lista)
    func(0,gramatical)

def p_sentencia_if_elif(t):
    'sentencia_if  : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lelseif'
    t[0] = If(t[3],t[6],[],t[8],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('sentencia_if ->IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lelseif','sentencia_if.instr = If(expresion,instruccionesV,lelseif);',lista)
    func(0,gramatical)

def p_lelseif(t):
    'lelseif    : lelseif elseif'
    t[1].append(t[2])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('lelseif -> lelseif elseif','lelseif.lista = lelseif1.lista; </hr> lelseif.lista.add(elseif);',[])
    func(2,gramatical)#func(0,gramatical)

def p_lelseif_s(t) :
    'lelseif    : elseif '
    t[0] = [t[1]]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('lelseif -> elseif','lelseif.lista = [elseif]',[])
    func(2,gramatical)#func(0,gramatical)

def p_elseif(t):
    'elseif : ELSE IF PARIZQ expresion PARDER LLAVIZQ  instrucciones LLAVDER '
    t[0] = If(t[4],t[7],[],[],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('elseif ->ELSE IF PARIZQ expresion PARDER LLAVIZQ  instrucciones LLAVDER','elseif.instr = If(expresion,instrucciones);',lista)
    func(0,gramatical)

#********************************************* SCAN *********************************************
def p_scan(t) :
    'ins_scan     : SCAN PARIZQ CADENA COMA PAND ID PARDER PTCOMA'
    op = Operacion()
    op.Indentficador(t[6],t.slice[6].lineno,find_column(t.slice[6]))

    opcad = Operacion()
    opcad.Primitivo(Primitivo(str(t[3]),t.slice[3].lineno,find_column(t.slice[3])))

    t[0] =Scan(opcad,op,t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('imprimir_instr ->IMPRIMIR PARIZQ CADENA COMA expresiones PARDER PTCOMA','imprimir_instr.instr = Print(CADENA,expresiones);',lista)
    func(0,gramatical)

#********************************************* IMPRIMIR *********************************************
def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ CADENA COMA expresiones PARDER PTCOMA'
    op = Operacion()
    op.Primitivo(Primitivo(str(t[3]),t.slice[3].lineno,find_column(t.slice[3])))
    t[0] =Imprimir(op,t[5],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('imprimir_instr ->IMPRIMIR PARIZQ CADENA COMA expresiones PARDER PTCOMA','imprimir_instr.instr = Print(CADENA,expresiones);',lista)
    func(0,gramatical)

def p_instruccion_imprimir_cad(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ CADENA PARDER PTCOMA'
    op = Operacion()
    op.Primitivo(Primitivo(str(t[3]),t.slice[3].lineno,find_column(t.slice[3])))
    t[0] =Imprimir(op,None,t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('imprimir_instr ->IMPRIMIR PARIZQ CADENA PARDER PTCOMA','imprimir_instr.instr = Print(CADENA);',lista)
    func(0,gramatical)

#********************************************** ASIGNACIONES *********************************************
def p_asignacion(t):
    'asignacion : ID IGUAL expresion  '
    t[0] = Asignacion(t[1],t[3],t.slice[2].lineno,1)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('asignacion -> ID IGUAL expresion PTCOMA','asignacion.instr = Asignar(ID.val,expresion.val);',lista)
    func(0,gramatical)

#********************************************** OPERACIONES DE ASIGNACION ******************************

def p_incre_decre(t):
    '''asignacion : ID MAS MAS
                  | ID MENOS MENOS '''
    op = Operacion()
    opId = Operacion()
    opId.Indentficador(t[1],t.slice[1].lineno,find_column(t.slice[1]))
    opId.linea = t.slice[1].lineno
    opId.columna = find_column(t.slice[1])

    opUno = Operacion()
    opUno.Primitivo(Primitivo(1,t.slice[1].lineno,find_column(t.slice[1])))


    if(t.slice[2].type == 'MAS'):
        op.Operacion(opId,opUno,TIPO_OPERACION.SUMA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID MAS MAS ','asignacion.instr = Asignar(ID.val,ID.val + 1);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MENOS'):
        op.Operacion(opId,opUno,TIPO_OPERACION.RESTA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID MENOS MENOS','asignacion.instr= Asignar(ID.val,ID.val - 1);',lista)
        func(0,gramatical)

    t[0] = Asignacion(t[1],op,t.slice[1].lineno,find_column(t.slice[1]))

def p_operaciones_asignacion(t):
    '''asignacion   :   ID ASUMA expresion 
                    |   ID ARESTA expresion  
                    |   ID MULTIPLICATIVA expresion 
                    |   ID DIVIDIDA expresion 
                    |   ID ARESTO expresion  
                    |   ID ABOR expresion  
                    |   ID APAND expresion 
                    |   ID ASHIFTD expresion 
                    |   ID ASHIFTI expresion 
                    |   ID AXORR expresion '''

    op = Operacion()
    opId = Operacion()
    opId.Indentficador(t[1],t.slice[1].lineno,find_column(t.slice[1]))
    opId.linea = t.slice[1].lineno
    opId.columna = find_column(t.slice[1])

    if(t.slice[2].type == 'ASUMA'):
        op.Operacion(opId,t[3],TIPO_OPERACION.SUMA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID MAS IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val + expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'ARESTA'):
        op.Operacion(opId,t[3],TIPO_OPERACION.RESTA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID MENOS IGUAL expresion','asignacion.instr= Asignar(ID.val,ID.val - expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MULTIPLICATIVA'):
        op.Operacion(opId,t[3],TIPO_OPERACION.MULTIPLICACION,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID MULT IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val * expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'DIVIDIDA'):
        op.Operacion(opId,t[3],TIPO_OPERACION.DIVISION,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID DIV IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val / expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'ARESTO'):
        op.Operacion(opId,t[3],TIPO_OPERACION.MODULO,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID RESTO IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val % expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'ABOR'):
        op.Operacion(opId,t[3],TIPO_OPERACION.BOR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID RESTO IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val | expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'APAND'):
        op.Operacion(opId,t[3],TIPO_OPERACION.PAND,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID RESTO IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val & expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'ASHIFTD'):
        op.Operacion(opId,t[3],TIPO_OPERACION.SHIFTD,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID RESTO IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val >> expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'ASHIFTI'):
        op.Operacion(opId,t[3],TIPO_OPERACION.SHIFTI,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID RESTO IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val << expresion.val);',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'AXORR'):
        op.Operacion(opId,t[3],TIPO_OPERACION.XORR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('asignacion ->  ID RESTO IGUAL expresion','asignacion.instr = Asignar(ID.val,ID.val ^ expresion.val);',lista)
        func(0,gramatical)

    t[0] = Asignacion(t[1],op,t.slice[1].lineno,find_column(t.slice[1]))

#********************************************** DECLARACIONES *********************************************

def p_declaracion(t):
    'declaracion : TIPO lista_id '
    t[0] = Declaracion(t[1],t[2],None,t.lexer.lineno,1)
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('declaracion -> TIPO LISTA_ID IGUAL expresion PTCOMA','declaracion.instr = Declaracion(TIPO,lista_id);',lista)
    func(0,gramatical)

def p_declaracion_asigna(t):
    'declaracion : TIPO lista_id IGUAL expresion  '
    t[0] = Declaracion(t[1],t[2],t[4],t.slice[3].lineno,find_column(t.slice[3]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('declaracion -> TIPO LISTA_ID IGUAL expresion PTCOMA','declaracion.instr = Declaracion(TIPO,lista_id,expresion.val);',lista)
    func(0,gramatical)

def p_lista(t) :
    'lista_id    : lista_id COMA ID'
    t[1].append(t[3])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('lista_id -> lista_id ID','lista_id.lista = lista_id1.lista; </hr> lista_id.lista.add('+t[3]+');',[])
    func(2,gramatical)#func(0,gramatical)

def p_lista_id(t) :
    'lista_id    : ID '
    t[0] = [t[1]]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('lista_id -> ID','instrucciones.lista = ['+t[1]+']',[])
    func(2,gramatical)#func(0,gramatical)

def p_tipo_dato(t):
    '''TIPO : INT 
                | FLOAT 
                | CHAR 
                | VOID '''

    if(t[1]=="int"):
        t[0] = Tipo.ENTERO
    elif(t[1]=="float"):
         t[0] = Tipo.FLOAT
    elif(t[1]=="char"):
         t[0] = Tipo.CHAR
    elif(t[1]=="void"):
         t[0] = Tipo.VOID
         
    gramatical = G.ValorAscendente('TIPO -> '+str(t[1]),'TIPO.val = '+str(t[1])+';',None)
    func(2,gramatical)


#*************************************************  EXPRESIONES  **************************************************

def p_expresiones(t):
    'expresiones : expresiones COMA expresion '
    t[1].append(t[3])
    t[0] = t[1]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresiones -> expresiones expresion','expresiones.lista = expresiones1.lista; </hr> expresiones.lista.add(expresion);',[])
    func(2,gramatical)#func(0,gramatical)

def p_expresiones_s(t):
    'expresiones : expresion '
    t[0] = [t[1]]
    #lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresiones -> expresion','expresiones.lista = [expresion]',[])
    func(2,gramatical)#func(0,gramatical)


def p_expresion(t):
    '''expresion : primitiva 
                 | expresion_numerica 
                 | expresion_relacional
                 | expresion_unaria
                 | expresion_logica 
                 | expresion_bit_bit '''
    t[0] = t[1]
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion -> '+str(t.slice[1]),'expresion.val = '+str(t.slice[1])+'.val;',lista)
    func(0,gramatical)

def p_expresion_parentesis(t):
    'expresion : PARIZQ expresion PARDER '
    t[0] = t[2]

#********************************************** OPERACIONES UNARIAS ***********************************
def p_expresion_unaria(t):
    'expresion_unaria   :   MENOS expresion %prec UMENOS' 
    op = Operacion()
    op.OperacionUnaria(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    t[0] = op
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion_unaria ->  MENOS expresion %prec UMENOS','expresion_unaria.val = -expresion.val;',lista)
    func(0,gramatical)
#********************************************** OPERACIONES LOGICAS ***********************************
def p_expresion_logica(t):
    '''expresion_logica   : expresion AND expresion 
                          | expresion OR expresion
                          | expresion XOR expresion '''
                          
    op = Operacion()
    if(t.slice[2].type == 'AND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.AND,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_logica ->  expresion AND expresion','expresion_logica.val = expresion1.val && expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'OR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.OR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_logica ->  expresion OR expresion','expresion_logica.val = expresion1.val || expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'XOR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.XOR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_logica ->  expresion XOR expresion','expresion_logica.val = expresion1.val xor expresion2.val;',lista)
        func(0,gramatical)
    t[0] = op

def p_expresion_negacion(t):
    'expresion_logica   :   NOT expresion %prec NOT' 
    op = Operacion()
    op.OperacionNot(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    t[0] = op    
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion_logica ->  NOT expresion %prec NOT','expresion_logica.val = !expresion.val;',lista)
    func(0,gramatical)
#********************************************** OPERACIONES BIT A BIT ***********************************
def p_expresion_bit_bit(t):
    '''expresion_bit_bit  : expresion PAND expresion 
                          | expresion BOR expresion
                          | expresion XORR expresion 
                          | expresion SHIFTI expresion
                          | expresion SHIFTD expresion'''
                          
    op = Operacion()
    if(t.slice[2].type == 'PAND'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.PAND,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  expresion PAND expresion','expresion_bit_bit.val = expresion1.val & expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'BOR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.BOR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  expresion BOR expresion','expresion_bit_bit.val = expresion1.val | expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'XORR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.XORR,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  expresion XORR expresion','expresion_bit_bit.val = expresion1.val ^ expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'SHIFTI'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SHIFTI,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  expresion SHIFTI expresion','expresion_bit_bit.val = expresion1.val << expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'SHIFTD'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SHIFTD,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_bit_bit ->  expresion SHIFTD expresion','expresion_bit_bit.val = expresion1.val >> expresion2.val;',lista)
        func(0,gramatical)
    t[0] = op

def p_expresion_negacion_bit(t):
    'expresion_bit_bit   :   NOTR expresion %prec NOTR' 
    op = Operacion()
    op.OperacionNotBit(t[2],t.slice[1].lineno,find_column(t.slice[1]))
    lista = func(1,None).copy()
    gramatical = G.ValorAscendente('expresion_bit_bit ->  NOTR expresion %prec NOTR','expresion_bit_bit.val = ~expresion.val;',lista)
    func(0,gramatical)
    t[0] = op   
#********************************************** OPERACIONES RELACIONALES ***********************************
def p_expresion_relacional(t):
    '''expresion_relacional :   expresion MENQUE expresion 
                            |   expresion MAYQUE expresion 
                            |   expresion MEIQUE expresion
                            |   expresion MAIQUE expresion
                            |   expresion IGUALQUE expresion 
                            |   expresion NIGUALQUE expresion '''
    op = Operacion()
    if(t.slice[2].type == 'MENQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  expresion MENOR expresion','expresion_relacional.val = expresion1.val < expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MAYQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  expresion MAYOR expresion','expresion_relacional.val = expresion1.val > expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MEIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MENOR_IGUA_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  expresion MENORIGUAL expresion','expresion_relacional.val = expresion1.val <= expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MAIQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MAYOR_IGUA_QUE,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  expresion MAYORIGUAL expresion','expresion_relacional.val = expresion1.val >= expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'IGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.IGUAL_IGUAL,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  expresion IGUAL IGUAL expresion','expresion_relacional.val = expresion1.val == expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'NIGUALQUE'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIFERENTE_QUE,t.slice[2].lineno,1)    
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_relacional ->  expresion DIFERENTE expresion','expresion_relacional.val = expresion1.val != expresion2.val;',lista)
        func(0,gramatical)
    t[0] = op
#********************************************** OPERACIONES ARITMETICAS ***********************************
def p_expresion_numerica(t):
    '''expresion_numerica   :   expresion MAS expresion 
                            |   expresion MENOS expresion 
                            |   expresion POR expresion
                            |   expresion DIVIDIDO expresion
                            |   expresion RESTO expresion'''

    op = Operacion()
    if(t.slice[2].type == 'MAS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.SUMA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  expresion MAS expresion','expresion_numerica.val = expresion1.val + expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'MENOS'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.RESTA,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  expresion MENOS expresion','expresion_numerica.val = expresion1.val - expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'POR'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MULTIPLICACION,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  expresion MULT expresion','expresion_numerica.val = expresion1.val * expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'DIVIDIDO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.DIVISION,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  expresion DIV expresion','expresion_numerica.val = expresion1.val / expresion2.val;',lista)
        func(0,gramatical)
    elif(t.slice[2].type == 'RESTO'):
        op.Operacion(t[1],t[3],TIPO_OPERACION.MODULO,t.slice[2].lineno,1)
        lista = func(1,None).copy()
        gramatical = G.ValorAscendente('expresion_numerica ->  expresion RESTO expresion','expresion_numerica.val = expresion1.val % expresion2.val;',lista)
        func(0,gramatical)
    t[0] = op

#********************************************** EXPRESIONES PRIMITIVAS ***********************************
def p_expresion_primitiva(t):
    '''primitiva : ENTERO
                 | DECIMAL
                 | CADENA
                 | CADENAR_CHAR
                 | ID '''

    op = Operacion()
    if(t.slice[1].type == 'CADENA' or t.slice[1].type == 'CADENAR_CHAR'):
        op.Primitivo(Primitivo(str(t[1]),t.slice[1].lineno,find_column(t.slice[1])))
        gramatical = G.ValorAscendente('primitiva -> CADENA','primitiva.val = str(CADENA);',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'DECIMAL'):
        op.Primitivo(Primitivo(float(t[1]),t.slice[1].lineno,find_column(t.slice[1])))
        gramatical = G.ValorAscendente('primitiva -> FLOAT','primitiva.val = float(FLOAT);',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'ENTERO'):
        op.Primitivo(Primitivo(int(t[1]),t.slice[1].lineno,find_column(t.slice[1])))
        gramatical = G.ValorAscendente('primitiva -> ENTERO','primitiva.val = int(ENTERO);',None)
        func(2,gramatical)
    elif(t.slice[1].type == 'ID') :
        op.Indentficador(t[1],t.slice[1].lineno,find_column(t.slice[1]))
        op.linea = t.slice[1].lineno
        op.columna = find_column(t.slice[1])
        gramatical = G.ValorAscendente('primitiva -> ID','primitiva.val = ID.val;',None)
        func(2,gramatical)
    t[0] = op


def p_error(t):
    try:
        error = Error.Error("SINTACTICO","Error sintactico, no se esperaba el valor "+t.value,t.lineno,find_column(t))
        ReporteErrores.func(error)
    except:
        error = Error.Error("SINTACTICO","Error sintactico",1,1)
        ReporteErrores.func(error)
    

parser = yacc.yacc()

def parse(input) :
    global lexer
    input = input.replace("\r","")
    lexer = lex.lex()
    return parser.parse(input)