# -*- coding: utf-8 -*-
"""
Autores:
    Adrian Montero Torralbo
    Alba Maria Montero Montero
    Sergio Semedi Barranco
Grupo YYY

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no haber
colaborado de ninguna manera con otros grupos, haber compartido el ćodigo con
otros ni haberlo obtenido de una fuente externa.
"""

from bottle import post, request, run, route, template
from pymongo import MongoClient
# Resto de importaciones...


# ¡MUY IMPORTANTE!
# Todas las inserciones se deben realizar en la colección 'users' dentro de la
# base de datos 'giw'.

client = None
db = None


def init():
	global client, db
	client = MongoClient()
	db = client['giw']


@route('/')
def index():
	return
	#quitar el comment si tienes el template
	#return template("index.tpl")

def insertaUsuario(id, country, cp, email, gender, likes, passw, year):
				
	db.users.insert({"_id" : id,
			"address": {
				"country": country,
				"zip": cp
				},
			"email": email,
			"gender": gender,
			"likes": likes,
			"password": passw,
			"year": year
		})

def modificaUsuario(id, country, cp, email, gender, likes, passw, year):
	

	result = db.users.update_one({"_id" : id},
			{
				"$set": {
					"address": {
						"country": country,
						"zip": cp
						},
					"email": email,
					"gender": gender,
					"likes": likes,
					"password": passw,
					"year": year
					}
			}
		)
   

				





@post('/add_user')
def add_user_post():
	
	id = request.forms.get('_id')
	
	if (db.users.find_one({"_id": id}) != None):
		return "el usuario ya existe"
	
  
	country = request.forms.get('country')
	cp = request.forms.get('zip')
	email = request.forms.get('email')
	gender = request.forms.get('gender')
	likes = request.forms.get('likes')
	passw = request.forms.get('password')
	year = request.forms.get('year')

	insertaUsuario(id, country, cp, email, gender, likes, passw, year)


	return "se ha creado el usuario"


@post('/change_email')
def change_email():
	global db
	id = request.forms.get('_id')
	email = request.forms.get('email')

	if (db.users.find_one({"_id": id}) == None):
		return "el usuario no existe"
	
	result = db.users.update_one({"_id" : id},
			{
				"$set": {
					"email": email
					}
			}
		)
	

	
	return "se ha modificado correctamente el correo"


@post('/insert_or_update')
def insert_or_update():
	id = request.forms.get('_id')
	country = request.forms.get('country')
	cp = request.forms.get('zip')
	email = request.forms.get('email')
	gender = request.forms.get('gender')
	likes = request.forms.get('likes')
	passw = request.forms.get('password')
	year = request.forms.get('year')

	if (db.users.find_one({"_id": id}) != None):
		modificaUsuario(id, country, cp, email, gender, likes, passw, year)
		return "se ha modificado el usuario"
	
	
	insertaUsuario(id, country, cp, email, gender, likes, passw, year)
	
	return "se ha creado el usuario"


@post('/delete')
def delete_id():
	

	id = request.forms.get('_id')

	if (db.users.find_one({"_id": id}) != None):
		print "se va a borrar el siguiente usuario: \n"
		print db.users.find_one({"_id": id})
		db.users.delete_one({"_id": id})
		return "se ha borrado el usuario (1)"

	return "el usuario que intenta borrar no existe"









@post('/delete_year')
def delete_year():
	global db
	year = request.forms.get('year')


	if (db.users.find_one({"year": year}) != None):
		result = db.users.delete_many({"year": year})
		return str(result.deleted_count)+ " usuarios eliminados"

	return "no hay ninguno en ese año"


	

init()
run(host='0.0.0.0', port=8080)
