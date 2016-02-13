# -*- coding: utf-8 -*-
"""
Autores: Sergio Semedi Barranco
        Alba Montero Monte
        Adrian Montero Torralbo
Grupo 7

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no haber
colaborado de ninguna manera con otros grupos, haber compartido el ćodigo con
otros ni haberlo obtenido de una fuente externa.
"""


from bottle import get, run, request, template
# Resto de importaciones

from pymongo import MongoClient
import json

client = MongoClient()
db = client.giw

@get('/find_user_id')
def find_user_id():

    # http://localhost:8080/find_user_id?_id=user_1


    id = request.GET.get('_id', '').strip()

    if (db.users.find_one({"_id": id}) == None):
		return "no existe ningun usuario"
    return template("users.tpl", rows = db.users.find({"_id": id}))


@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?gender=Male
    # http://localhost:8080/find_users?gender=Male&year=2009

    dict = request.query.decode();

    #el metodo funciona correctamente pero tiene el problema de que
    #los anyos los sigue tratando como string y no coinciden con integer

    #intento fallido de castear los valores a int:
    #if ("year" in dict.keys()):
    #    for doc in dict:
    #        for key in doc:
    #            doc[key] = int(doc[key])



    table = db.users.find(dict)



    if (table.count() == 0):
		return "no existe ningun usuario"


    return template("users.tpl", rows = table, n = table.count())


@get('/find_users_or')
def find_users_or():
    # http://localhost:8080/find_users_or?gender=Male&year=2000

    dict = request.query.decode();

    info = []
    for doc in dict:
        info.append({doc:dict[doc]})




    table = db.users.find({"$or": info})


    if (table.count() == 0):
		return "no existe ningun usuario"


    return template("users.tpl", rows = table, n = table.count())



@get('/find_like')
def find_like():
    # http://localhost:8080/find_like?like=football
    like = request.GET.get('like', '').strip()

    table = db.users.find({"likes": {"$all": [like]}})

    if (table.count()== 0): return "no hay nadie con ese gusto"


    return template("users.tpl", rows = table, n = table.count())


@get('/find_country')
def find_country():
    # http://localhost:8080/find_country?country=Spain

    country= request.GET.get('country', '').strip()


    table = db.users.find({"address.country": country})

    if (table.count()== 0): return "no hay nadie con ese pais"
    return template("users.tpl", rows = table, n = table.count())


@get('/find_email_year')
def email_year():
    # http://localhost:8080/find_email_year?year=1992
    year = request.GET.get('year', '').strip()


    table = db.users2.find({"year": int(year)}, {"_id": 1, "email":1})
    if (table.count()== 0): return "no hay nadie "

    return template("users.tpl", rows = table, n = table.count())


@get('/find_country_limit_sorted')
def find_country_limit_sorted():
    # http://localhost:8080/find_country_limit_sorted?country=Spain&limit=20&ord=asc
    ord = request.GET.get('ord', '').strip()
    country= request.GET.get('country', '').strip()
    limit = request.GET.get('limit', '').strip()

    table = db.users.find({"address.country": country})
    n=0

    if (table.count()== 0): return "no hay nadie "

    if (ord == "asc"):n=1
    elif (ord == "desc"):n=-1
    return template("users.tpl", rows = table.sort("year", n).limit(int(limit)), n = table.count())


###############################################################################
################# Funciones auxiliares a partir de este punto #################
###############################################################################





###############################################################################
###############################################################################

if __name__ == "__main__":

    run(host='localhost',port=8080,debug=True)
