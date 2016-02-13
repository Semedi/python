class entry:
        def __init__(self, nombre, apellidos, telefono):
                self.n = nombre
                self.a = apellidos
                self.t = telefono
        
        def __str__(self):
                return self.n + "\n" + self.a + "\n" + self.t + "\nXXX\n"
                

_entrys = []
_file = False


def Update():
        out = open("agenda.txt","w")
        for entrada in _entrys:
                out.write(str(entrada))
        
        out.close()
        
        
        

def EscribirEntrada(entrada):
        global _file
        
        if _file:
                out = open("agenda.txt", "a")
        else:
                out = open("agenda.txt", "w")
                _file = True
                
        out.write(str(entrada))
        out.close()

def CrearEntrada():
        print "Nombre: "
        nombre = raw_input()

        print "Apellidos: "
        apellidos = raw_input()

        print "Telefono: "
        telefono = raw_input()
        
        entrada = entry(nombre, apellidos, telefono)
        _entrys.append(entrada)
        EscribirEntrada(entrada)
        


def BorrarEntrada():

        if _file:
                delete=raw_input('Nombre y apellidos de la persona a eliminar: ')
                
                for entrada in _entrys:
                        if delete == entrada.n +" "+ entrada.a:
                                _entrys.remove(entrada)
                Update()
        else:
                print('Antes de borrar, cargue el archivo (4). \n')
                

def BuscarEntrada():
        if _file:
                search=raw_input('Busqueda: ')
                for entrada in _entrys:
                        if search in entrada.n or search in entrada.a:
                                print entrada
                #print('La busqueda no dio resultados. \n')
        else:
                print('Antes de buscar, cargue el archivo (4). \n')

def CargarEntrada():
        global _file

        try:
                agenda = open("agenda.txt", "r")
                cont=0
                
                while True:
                        nombre = agenda.readline().strip("\n")
                        if nombre == "":
                                break
                        apellidos = agenda.readline().strip("\n")
                        telf = agenda.readline().strip("\n")
                        _entrys.append(entry(nombre, apellidos, telf))
                        aux = agenda.readline()
                        
                agenda.close()
                _file = True
                print('Agenda cargada con exito. \n')
        except:
                print('No existe el archivo, o no se ha podido abrir. \n')
                        
        
        

def agenda():
    ans=True
    while ans:
        print "1.Crear entrada"
        print "2.Borrar entrada"
        print "3.Buscar entrada"        
        print "4.Cargar entrada"
        print "5.Salir"

        opt=raw_input('Opcion: ')
        if opt == '1':
                CrearEntrada()                          
        elif opt == '2':
                BorrarEntrada()
        elif opt == '3':
                BuscarEntrada()
        elif opt == '4':
                CargarEntrada()
        elif opt == '5':
                ans=False
                

agenda()
