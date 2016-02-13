import urllib
from xml.etree import ElementTree

def tratarDatos(fileName):
    f = open(fileName, "rt")
    arbol = ElementTree.parse(f)
    for nodo in arbol.iter():
        if (nodo.tag == "formatted_address"):
            print nodo.text
        elif ()

def crearXML(fileName, data):
        f = open(fileName, "w")
        for entrada in data:
                f.write(str(entrada))
                
def programa ():
        salir = False
        while (salir == False):
            busqueda = raw_input('Introduce tu busqueda ("stop" para salir) \n')
            if (busqueda != 'stop'):
                serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'
                url = serviceurl + urllib.urlencode({'sensor':'false', 'address': busqueda})
                networkObj = urllib.urlopen(url)
                data = networkObj.read()
                crearXML(busqueda + '.xml', data)
                tratarDatos(busqueda + '.xml')
            else:
                break

programa()
