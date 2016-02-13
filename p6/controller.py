import sqlite3
import model
import cookielib
from bottle import route, run, template, error, static_file, request,response,redirect


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
        response.set_cookie("id",id,secret='key')
        return template("template/success.tpl",menu='success')
    except:
        return template("template/fail.tpl",menu='fail')

@route('/catalogo')
def catalogo():
    db = sqlite3.connect('gestorLibros.sqlite3')
    c = db.cursor()
    c.execute("SELECT * FROM Libros")
    data = c.fetchall()
    c.close()
    return template("template/catalogo.tpl", rows = data,menu='catalogo')

@route('/expire')
def expire():
    response.set_cookie("id", None, secret='key' , expires=0)
    redirect("/")

@route('/gestion')
def gestion():
    db = sqlite3.connect('gestorLibros.sqlite3')
    c = db.cursor()
    userId = request.get_cookie("id", secret='key')
    c.execute('SELECT id_lib FROM Usuario_tiene_libro WHERE id_u = ?',[userId])
    data=c.fetchall()
    lista=[]
    for id in data:
            c.execute('SELECT * from Libros WHERE id = ?', id)
            lista.append(c.fetchall()[0])
            
    return template("template/gestion.tpl",rows = lista, menu='gestion')

@route('/doGestion')
def do_gestion():
    db = sqlite3.connect('gestorLibros.sqlite3')
    c = db.cursor()
    if '1' in request.query['eliminar']:
        userId = request.get_cookie("id", secret='key')
        productId = request.query['id']
        c.execute('DELETE FROM Usuario_tiene_libro WHERE id_U = ? AND id_lib = ?',[userId, productId])
        db.commit()
        redirect("/gestion")
    else:
        return "modificar"
@route('/comprar', method ='POST')
def comprar():
    bookId = request.forms.get('id')
    userId = request.get_cookie("id", secret='key')
    db = sqlite3.connect('gestorLibros.sqlite3')
    c = db.cursor()
    c.execute('INSERT INTO Usuario_tiene_libro VALUES(?,?)',(userId,bookId))
    db.commit()
    redirect("/gestion")

@route('/registro')
def registro():
    return template("template/registro.tpl", menu='index')

@route('/registro', method = 'POST')
def do_registro():
    username = request.forms.get('user')
    password = request.forms.get('password')

    db = sqlite3.connect('gestorLibros.sqlite3')
    c = db.cursor()
    c.execute('SELECT id from Usuarios')
    n = len(c.fetchall())+1

    c.execute('INSERT INTO Usuarios VALUES (?,?,?)', (n,username,password))
    db.commit()
    redirect("/")

@route('/busqueda')
def busqueda():
    return template("template/busqueda.tpl", menu='busqueda')



@route('/busqueda', method = 'POST')
def tratarBusqueda():
    busqueda = request.forms.get('searchterm')
    columna = request.forms.get('campo')
    column = str(columna)
    search= "%"+str(busqueda)+"%"
    db = sqlite3.connect('gestorLibros.sqlite3')
    c=db.cursor()
    if column == "Titulo":
        c.execute('SELECT * FROM Libros WHERE Titulo LIKE ? ',[search])
    elif column == "Autor":
        c.execute('SELECT * FROM Libros WHERE Autor LIKE ? ',[search])
    elif column == "Categoria":
        c.execute('SELECT * FROM Libros WHERE Categoria LIKE ? ',[search])
    idS = c.fetchall()
    return template("template/resulBusqueda.tpl",rows = idS, menu='busqueda')


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@error(404)
def error404(error):
    return 'Error en la pagina solicitada'


model.initDB()
run(host='0.0.0.0', port=8080)
