import json

def cargar():
    archivo = open("tweets.txt")
    terminos = {}

    cnt = 0
    for line in  archivo.readlines():
        pythonData = json.loads(line)
        contenidoTweet= pythonData.get('text')
        #print pythonData.get('text')
        if contenidoTweet!= None:
            contenidoTweet.encode('UTF-8')
            palabras = contenidoTweet.split()
            cnt = cnt + len(palabras)
            for i in range (0, len(palabras)):
                if terminos.has_key(palabras[i]):
                    terminos[palabras[i]]= terminos[palabras[i]]+1
                else: terminos[palabras[i]]=1
        else: continue
    salida = open("frecuenciaTerminos.txt", "w")
    for key in terminos:
        salida.write(key.encode('UTF-8') + " " + str(terminos[key]/float(cnt)) + '\n' ) #numero de veces que aparece la palabra                                 
      #

    salida.close()

    

cargar()
