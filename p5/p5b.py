import urllib
from BeautifulSoup import *

def buscador():
    url = "http://trenesytiempos.blogspot.com.es/"
    while True:
        palabras = raw_input('Introduce las palabra a buscar (separadas por espacios ",") introduce 0 para salir: ')
        if palabras =='0':
            break
        else:
            html = urllib.urlopen(url).read()
            sopa = BeautifulSoup(html)
            entradas = sopa('a',{"class:post-count-link"},"html5lib")
            palabras.split()
            if len(palabras)>1:
               for palabra in palabras:
                   
            else:
                
            print html
            
buscador()
                    
