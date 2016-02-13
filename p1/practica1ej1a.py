
def cifradoCesar(cadena, desplazamiento):
    
    print('Mensaje a cifrar: '+ cadena)
    cifrado = ""

    for c in cadena.lower():
        if (ord(c) >= ord('a')) and (ord(c) <= ord('z')):
            if(ord(c) > ord('z')- desplazamiento):
                cifrado = cifrado + unichr(ord('a') + desplazamiento - (ord('z')- ord(c))-1)
            else:
                cifrado = cifrado + unichr(ord(c)+ desplazamiento)
        else:
            cifrado = cifrado + cifrado
    print ('Mensaje cifrado: '+ cifrado)

def init():
    ans = True
    while ans:
        cadena = raw_input('Inserta un mensaje a cifrar (0 para salir) \n')
        entero = False
        if (cadena != '0'):
            while (entero == False):
                try: 
                    desplazamiento = raw_input('Inserta un desplazamiento \n')
                    desp = int(desplazamiento)
                    entero = True
                except:
                    entero = False
                    print'Por favor, introduzca un entero'
            cifradoCesar(cadena, desp)
        else:
            ans = False
    

init()
