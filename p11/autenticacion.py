# -*- coding: utf-8 -*-
"""
Autores: Alba Mª Montero Monte
         Sergio Alfonso Semedi Barranco
         Adrián Montero Torralbo
Grupo 007

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
"""

from bottle import run, post, request, template, route
# Resto de importaciones
from pymongo import MongoClient
import hashlib
import uuid
import json
###########################
import string
import random
import onetimepass as otp
###########################
client= MongoClient()
db = client.giw


@route('/')
def index():
    return template('index.tpl')
@route('/index2')
def index2():
    return template('index2.tpl')

##############
# APARTADO A #
##############


@post('/signup')
def signup():
    
    _id = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    passw = request.forms.get('password')
    passw2 = request.forms.get('password2')

    if (passw != passw2):
        return "Las contraseñas no coinciden"
    elif (db.users.find_one({"_id": _id})): #existe usuario
            return "El alias de usuario ya existe"
    else:
        #inserta usuario
        #hacer hash con sal
        salt = uuid.uuid4().hex
        new_pass = hash_password(passw, salt)
        print('The string to store in the db is: '+ new_pass)
        db.users.insert_one({"_id": _id, "name": name, "country":country, "email":email, "password":new_pass, "password2":passw2, "salt":salt})
        return "Bienvenido usuario " + name

@post('/change_password')
def change_password():
    
    _id = request.forms.get('nickname')
    passw = request.forms.get('old_password')
    passw2 = request.forms.get('new_password')
    resul = db.users.find_one({"_id":_id}, {"password":1, "salt":1})
    print resul
    if (resul != None):
        salt = resul["salt"]
        old_pass = resul["password"]
        old_passw_in = hash_password(passw, salt)
        if(old_passw_in == old_pass):
            new_pass = hash_password(passw2, salt)       
            db.users.update_one({"_id":_id}, {"$set":{"password": new_pass, "password2":new_pass}})
            return "La contraseña del usuario "+ _id + " ha sido modificada"
        else: return "Usuario o contrasenia incorrectos(passw)"
    else : return "Usuario o contrasenia incorrectos(user)"

@post('/login')
def login():
    _id = request.forms.get('nickname')
    passw = request.forms.get('password')
    resul = db.users.find_one({"_id":_id}, {"password":1, "name":1, "salt":1})
    if(resul != None):
        salt = resul["salt"]
        old_pass = resul["password"]
        old_passw_in = hash_password(passw, salt)
        if(old_passw_in == old_pass):
            return "Bienvenido "+ resul["name"]
        else: return "Usuario o contrasenia inconrrectos(passw)"
    else: return "Usuario o contrasenia incorrectos(user)"

##############
# APARTADO B #
##############


def gen_secret():
    # Genera una cadena aleatoria de 16 caracteres a escoger entre las 26 
    # letras mayúsculas del inglés y los dígitos 2, 3, 4, 5, 6 y 7. 
    #
    # Ejemplo:
    # >>> gen_secret()
    # '7ZVVBSKR22ATNU26'
    number = '234567'
    chars = string.ascii_uppercase + number
    size = 16
    return ''.join(random.choice(chars) for _ in range(size))
    
    
def gen_gauth_url(app_name, username, secret):
    # Genera la URL para insertar una cuenta en Google Authenticator
    #
    # Ejemplo:
    # >>> gen_gauth_url( 'GIW_grupoX', 'pepe_lopez', 'JBSWY3DPEHPK3PXP')
    # 'otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX
    #    
    # Formato de la URL:
    # otpauth://totp/<ETIQUETA>?secret=<SECRETO>&issuer=<NOMBRE_APLICACION_WEB>
    #
    # Más información en: 
    #   https://github.com/google/google-authenticator/wiki/Key-Uri-Format
    return 'otpauth://totp/'+username+'?secret='+secret+'&issuer='+app_name
        

def gen_qrcode_url(gauth_url):
    # Genera la URL para generar el código QR que representa 'gauth_url'
    # Información de la API: http://goqr.me/api/doc/create-qr-code/
    #
    # Ejemplo:
    # >>> gen_qrcode_url('otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX')
    # 'http://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2Fpepe_lopez%3Fsecret%3DJBSWY3DPEHPK3PXP%26issuer%3DGIW_grupoX'
    url = ''
    for i in range(0, len(gauth_url)):
        if (gauth_url[i] == ':'):
             url += '%3A'
        elif(gauth_url[i] == '/'):
             url += '%2F'
        elif(gauth_url[i] == '?'):
             url += '%3F'
        elif(gauth_url[i] == '='):
             url += '%3D'
        elif(gauth_url[i] =='&'):
             url += '%26'
        else: url += gauth_url[i]
    print url
    return''+'http://api.qrserver.com/v1/create-qr-code/?data=' + url
    


@post('/signup_totp')
def signup_totp():
    _id = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    passw = request.forms.get('password')
    passw2 = request.forms.get('password2')

    if (passw != passw2):
        return "Las contraseñas no coinciden"
    elif (db.users.find_one({"_id": _id})): 
            return "El alias de usuario ya existe"
    else:
        salt = uuid.uuid4().hex
        new_pass = hash_password(passw, salt)
        seed = gen_secret()
        url=gen_qrcode_url(gen_gauth_url('GIW_grupo7', name, seed))
        db.users.insert_one({"_id": _id, "name": name, "country":country, "email":email, "password":new_pass, "password2":passw2, "salt":salt, "secret":seed})
        return template("qr-code.tpl",userName = name, secret = seed, qr = url)
        
        
@post('/login_totp')        
def login_totp():
    _id = request.forms.get('nickname')
    passw = request.forms.get('password')
    resul = db.users.find_one({"_id":_id}, {"password":1, "name":1, "salt":1, "secret":1})
    if(resul != None):
        salt = resul["salt"]
        old_pass = resul["password"]
        old_passw_in = hash_password(passw, salt)
        if(old_passw_in == old_pass):
            toptp=otp.get_totp(resul["secret"],as_string=True)
            if(otp.valid_toptp(toptp,resul["secret"])):
                return "Bienvenido "+ resul["name"]
            else: return "Usuario o contrasenia inconrrectos(totp)"
        else: return "Usuario o contrasenia inconrrectos(passw)"
    else: return "Usuario o contrasenia incorrectos(user)"
#############################
    ####FUNCIÓN DE HASH PARA LA CONTRASEÑA####
def hash_password(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


    
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)

