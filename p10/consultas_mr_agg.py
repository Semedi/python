# -*- coding: utf-8 -*-
"""
Autores: Sergio Semedi Barranco
        Alba Montero Monte
        Adrian Montero Torralbo
Grupo 07

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no haber
colaborado de ninguna manera con otros grupos, haber compartido el ćodigo con
otros ni haberlo obtenido de una fuente externa.
"""


# Importaciones
from bottle import get, run, template
from pymongo import MongoClient
from bson.code import Code
from bson.son import SON

client = MongoClient()
db = client.giw

# MapReduce: usuarios en cada pais.
@get('/users_by_country_mr')
def users_by_country_mr():



    mapper  = Code("""
                    function() {
                        emit(this.country, 1);
                    }
                    """)

    reducer = Code("""
                    function (key, values) {
                        var total = 0;
                        for (var i = 0; i < values.length; i++) {
                            total += values[i];
                        }
                        return total;
                    }
                    """)

    table = db.users.map_reduce(mapper, reducer,"nPaises")


    return template("users.tpl", rows = table.find(), columns = ["Pais", "Num.Usuarios"])

# Aggregation Pipeline: usuarios en cada pais (orden descendente por numero
# de usuarios).
@get('/users_by_country_agg')
def users_by_country_agg():

    pipeline = [
                {"$group": {"_id" :"$country", "num": {"$sum":1}}},
                {"$sort": SON ([("num", -1)])}
                ]

    table = db.command('aggregate', 'users', pipeline = pipeline)


    return template("users.tpl", rows = table["result"], columns = ["Pais", "Num.Usuarios"])


# MapReduce: gasto total en cada pais.
@get('/spending_by_country_mr')
def spending_by_country_mr():

        mapper  = Code("""
                        function() {
                            var key = this.country;
                            var value = 0;
                            if (this.orders){
                                    for (var idx = 0; idx < this.orders.length; idx++){
                                        value += this.orders[idx].total;
                                    }
                            }


                            emit(key, value);
                        }
                        """)

        reducer = Code("""
                    function (key, values) {
                        var total = 0;
                        for (var i = 0; i < values.length; i++) {
                            total += values[i];
                        }
                        return total;
                    }
                    """)




        table = db.users.map_reduce(mapper, reducer,"totalPaises")

        return template("users.tpl", rows = table.find(), columns = ["Pais", "gasto total"])


# Aggregation Pipeline: gasto total en cada pais (orden descendente por nombre
# del pais).
@get('/spending_by_country_agg')
def spending_by_country_agg():

        pipeline = [
                    {"$unwind": "$orders" },
                    {"$group": {"_id" :"$country", "num": {"$sum": "$orders.total"}}},
                    {"$sort": SON ([("_id", 1)])}
        ]

        table = db.command('aggregate', 'users', pipeline = pipeline)

        return template("users.tpl", rows = table["result"], columns = ["Pais", "gasto total"])



# MapReduce: gasto total realizado por las mujeres que han realizdo EXACTAMENTE
# 3 compras.

@get('/spending_female_3_orders_mr')
def spending_female_3_orders_mr():
                mapper  = Code("""
                            function() {
                            var key = this.gender = "Female";
                            var value = 0;
                            if (this.orders){
                                if(this.orders.length == 3){
                                    for (var idx = 0; idx < this.orders.length; idx++){
                                        value += this.orders[idx].total;
                                    }
                                }
                            }


                            emit(key, value);
                        }
                        """)

                reducer = Code("""
                                function(key, values) {
                                var total = 0;
                                for (var i = 0; i < values.length; i++) {
                                    total += values[i];
                                }
                            return total;
                            }
                            """)




                table = db.users.map_reduce(mapper, reducer,"totalGastos")
                rows = table.find()
                for i in rows:
                        for j in i:
                           Gasto_total =  i[j]
                return "El gasto total es "+ str(Gasto_total)






# Aggregation Pipeline: gasto total realizado por las mujeres que han realizdo
# EXACTAMENTE 3 compras.
@get('/spending_female_3_orders_agg')
def spending_female_3_orders_agg():

     pipeline = [
               
                  {"$project": {"n": {"$size": { "$ifNull": [ "$orders", [] ] }},"orders.total":1, "gender": 1}},
                  {"$match" : {"$and":[{"gender":"Female"},{ "n" : 3 }]}},
                  {"$unwind": "$orders" },
                  {"$group": {"_id" :"$gender", "Gasto_total": {"$sum": "$orders.total"}}},
                  {"$sort": SON ([("Gasto_total",-1)])}
    ]
     
    # print numOrders
     table = db.command('aggregate', 'users', pipeline = pipeline)
     rows = table["result"]
     for i in rows:
         for j in i:
             if(j == "Gasto_total"):
                gasto_total = i[j]
            # print str(i[j]) + " i=" +str(i) + " j=" +str(j)
     return "el gasto total es "+ str(gasto_total)




###############################################################################
###############################################################################

if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
