import urllib
import xml.dom.minidom
from xml.dom.minidom import parse


class site:
    def __init__(self):
        self.name =""
        self.country =""
        self.short =""
        self.lvl ="Ninguna"
        self.address =""
        self.lat =""
        self.lon =""

    def setName(self,name):
        self.name = name.encode("UTF-8")

    def setCountry(self, country, short):
        self.country = country.encode("UTF-8")
        self.short = short.encode("UTF-8")

    def setlvl(self, lvl):
        self.lvl=lvl.encode("UTF-8")

    def setAddress(self, a):
        self.address =a.encode("UTF-8")

    def setCords(self, x, y ):
        self.lon=x.encode("UTF-8")
        self.lat=y.encode("UTF-8")
        
    def __str__(self):
        return "Informacion: \n Nombre: "+self.name+"\n Pais: "+self.country+"\n Nombre corto de pais: "+self.short+"\n Entidad de nivel 1: "+self.lvl+"\n Direccion formateada: "+self.address+"\n Longitud: "+self.lon+" Latitud: "+self.lat


serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'

def tratarDatos(fileName):
        ArbolDOM = xml.dom.minidom.parse(fileName)
        geocode = ArbolDOM.documentElement

        status = geocode.getElementsByTagName("status")[0].childNodes[0].data
        if(status != "OK"):
            print ("Busqueda fallida.")
            return
        componentes = geocode.getElementsByTagName("address_component")
        sitio = site()
        
        #este for es para recorrer todos los address componente (en ellos necesitamos sacar info de ciertas etiquetas)
        for componente in componentes:
            type = componente.getElementsByTagName("type")[0]
            typeText = type.childNodes[0].data

            if typeText == "locality":
                sitio.setName(componente.getElementsByTagName("short_name")[0].childNodes[0].data)
            elif typeText == "country":
                sitio.setCountry(componente.getElementsByTagName("long_name")[0].childNodes[0].data,  componente.getElementsByTagName("short_name")[0].childNodes[0].data)
            elif typeText == "administrative_area_level_1":
                sitio.setlvl(componente.getElementsByTagName("long_name")[0].childNodes[0].data)

        sitio.setAddress(geocode.getElementsByTagName("formatted_address")[0].childNodes[0].data)
        location=geocode.getElementsByTagName("geometry")[0].getElementsByTagName("location")[0]      
        sitio.setCords(location.getElementsByTagName("lng")[0].childNodes[0].data ,location.getElementsByTagName("lat")[0].childNodes[0].data)

        print(sitio)
    


def crearXML(fileName, data):
    try:
        f = open(fileName, "w")
        for entrada in data:
                f.write(str(entrada))
    except IOError:
        print("Busqueda incluye caracteres no validos (\/:*?\"<>|) \n")
        return False
    return True

def programa ():
        while True:
            busqueda = raw_input('Introduce tu busqueda ("stop" para salir): \n')
            if (busqueda != 'stop'):
                if(len(busqueda)>= 1):
                    try:
                        url = serviceurl + urllib.urlencode({'sensor':'false', 'address': busqueda})
                        networkObj = urllib.urlopen(url)
                        data = networkObj.read()
                    except IOError:
                        print("No tienes conexion a internet. \n")
                        exit()
                    if(crearXML(busqueda+'.xml', data)):
                        tratarDatos(busqueda+'.xml')
                else:
                    print("Introduce una busqueda valida. \n")
            else:
                break

programa()
