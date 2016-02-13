import urllib
import os
import re
from bs4 import BeautifulSoup


def procesaEntrada(ref):
    html = urllib.urlopen(ref).read()
    s = BeautifulSoup(html)
    etiquetas = s('a',{"imageanchor":"1"})

    j=0

    for i in etiquetas:
        archivo = open("foto"+str(j)+".jpg","wb")
        imagen=urllib.urlopen(i.get('href', None))
        while True:
            info = imagen.read(100000)
            if len(info) < 1: break
            archivo.write(info)
        archivo.close()
        j+=1

#O(n^2)
def ej1():
    print "\n Creando directorios y descargando contenido...\n"
    try:
        html = urllib.urlopen('http://trenesytiempos.blogspot.com.es/').read()
    except:
        print "Error: no se pudo realizar la conexion"
        return
    soup = BeautifulSoup(html, "html5lib")

    links = soup('a',{"class":"post-count-link"},"html5lib")

    j=-1

    for i in links:

        j+=1

        if (not(j)): continue
        if ("2014" in str(i)): break
        dir="entrada"+str(j)
        if (not(os.path.exists(dir))): os.makedirs(dir)
        os.chdir(dir)
        procesaEntrada(i['href'])
        os.chdir('..')
        print "Guardada entrada" + str(j)

    print "\n Ejecucion terminada."

def buscaPalabras(link, palabras):
    html = urllib.urlopen(link).read()
    soup = BeautifulSoup(html, "html5lib")

    encontrado = True
    for i in palabras:
        if (not(encontrado)): break
        columns = soup.find(text = re.compile(i))
        encontrado = encontrado and (columns != None)

    return encontrado

#O(n^2)
def buscador(palabras):
    print "\n Buscando...\n"
    try:
        html = urllib.urlopen('http://trenesytiempos.blogspot.com.es/').read()
    except:
        print "Error: no se pudo realizar la conexion"
        return
    soup = BeautifulSoup(html, "html5lib")

    links = soup('a',{"class":"post-count-link"},"html5lib")
    for i in links:
        if ("search" in str(i)): continue
        if (buscaPalabras(i['href'], palabras)):
           print i['href']

def ej2():

    while True:
        palabras = raw_input('Introduce las palabras a buscar (separadas por coma; 0 para salir): ')
        if (palabras == '0'):
            print "Error: no ha introducido ninguna palabra."
            return
        else: buscador(palabras.split(','))

        print "\n Ejecucion terminada. \n"



if __name__ == '__main__':
    ans=True
    while ans:
        print "1.Recopilar fotos del blog (ej1)"
        print "2.Busqueda de palabras (ej2)"
        print "0. Salir"


        opt=raw_input('Opcion: ')

        if (opt=='0'): ans=False
        elif (opt == '1'): ej1()
        elif (opt == '2'): ej2()
