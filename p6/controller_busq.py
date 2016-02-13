import sqlite3
import model
from bottle import route, run, template, error, static_file, request


@route('/')
def index():
    return template("template/index.tpl", menu='index')

@route('/',method='POST')
def do_login():
    username = request.forms.get('user')
    password = request.forms.get('password')

    db = sqlite3.connect('gestorLibros.sqlite3')
    c=db.cursor()
    c.execute('SELECT id FROM Usuarios WHERE mail = ? AND Password = ? LIMIT 1', (username, password))
    try:
        id = c.fetchone()[0]
        return "<p>Login correcto</p>"
    except:
        return "<p>Login incorrecto.</p>"

@route('/catalogo')
def catalogo():
    db = sqlite3.connect('gestorLibros.sqlite3')
    c = db.cursor()
    c.execute("SELECT * FROM Libros")
    data = c.fetchall()
    c.close()
    return template("template/catalogo.tpl", rows = data,menu='catalogo')

@route('/gestion')
def gestion():
    return template("template/gestion.tpl", menu='gestion')

@route('/registro')
def registro():
    return template("template/registro.tpl", menu='index')

@route('/busqueda')
def busqueda():
    return template("template/busqueda.tpl", menu='busqueda')

@route('/busqueda', method = 'POST')
def tratarBusqueda():
    busqueda = request.forms.get('searchterm')
    columna = request.forms.get('campo')
    db = sqlite3.connect('gestorLibros.sqlite3')
    c=db.cursor()
    c.execute('SELECT * FROM Libros WHERE ? = ?', (columna, busqueda))
    data = c.fetchall()
    c.close()

    #return template("template/busqueda.tpl", menu='busqueda')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@error(404)
def error404(error):
    return 'Error en la pagina solicitada'


model.initDB()
run(host='0.0.0.0', port=8080)
