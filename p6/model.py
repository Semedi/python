# -*- coding: utf-8 -*-
import sqlite3
def initDB():
    db = sqlite3.connect('gestorLibros.sqlite3')
    db.execute("DROP TABLE IF EXISTS Usuarios")
    db.execute("DROP TABLE IF EXISTS Libros")
    db.execute("DROP TABLE IF EXISTS Usuario_tiene_libro")
    db.execute("CREATE TABLE Usuarios(id INTEGER PRIMARY KEY,mail CHAR(100) UNIQUE, Password CHAR(100))")
    db.execute("CREATE TABLE Libros(id INTEGER PRIMARY KEY,Titulo CHAR(100), Autor CHAR(100), Categoria CHAR(100))")
    db.execute("CREATE TABLE Usuario_tiene_libro(id_u INTEGER REFERENCES Usuarios,id_lib INTEGER REFERENCES Libros, CONSTRAINT contiene_PK PRIMARY KEY (id_u, id_lib))")

    db.execute("INSERT INTO Libros VALUES(100,'Juego de Tronos', 'George Martin', 'Fantasia')")
    db.execute("INSERT INTO Libros VALUES(101,'Choque de Reyes', 'George Martin', 'Fantasia')")
    db.execute("INSERT INTO Libros VALUES(102,'Tormenta de Espadas', 'George Martin', 'Fantasia')")
    db.execute("INSERT INTO Libros VALUES(103,'Festin de Cuervos', 'George Martin', 'Fantasia')")
    db.execute("INSERT INTO Libros VALUES(104,'Danza de dragones', 'George Martin', 'Fantasia')")
    db.execute("INSERT INTO Libros VALUES(105,'Un mundo feliz', 'Aldous Huxley', 'Contemporanea')")
    db.execute("INSERT INTO Libros VALUES(106,'1984', 'George Orwell', 'Contemporanea')")
    db.execute("INSERT INTO Libros VALUES(107,'Farenheit 451', 'Ray Bradbury', 'Contemporanea')")
    db.execute("INSERT INTO Libros VALUES(108,'Rebelión en la granja', 'George Orwell', 'Contemporanea')")

    db.execute("INSERT INTO Usuarios VALUES(1, 'admin@admin.com','admin')")
    db.execute("INSERT INTO Usuarios VALUES(2, 'carmen@carmen.com','carmen')")

    db.execute("INSERT INTO Usuario_tiene_libro VALUES(2,100)")
    db.commit()

