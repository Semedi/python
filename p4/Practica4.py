def login(dbfile):
    import sqlite3
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    return conn, cur


#apartado 1
def crearTablas(cur):
    cur.execute("DROP TABLE IF EXISTS Universidades")
    cur.execute("DROP TABLE IF EXISTS Estudiantes")
    cur.execute("DROP TABLE IF EXISTS Solicitudes")
    cur.execute("CREATE TABLE Universidades(Nombre_Univ TEXT PRIMARY KEY, Comunidad TEXT, Plazas INTEGER)")
    print ('Tabla "Universidades" creada con exito en ' + dbfile)
    cur.execute("CREATE TABLE Estudiantes(id INTEGER PRIMARY KEY, Nombre_Est TEXT, Nota REAL, Valor INTEGER)")
    print ('Tabla "Estudiantes" creada con exito en ' + dbfile)
    cur.execute("CREATE TABLE Solicitudes(id INTEGER CONSTRAINT sol_id REFERENCES Estudiantes,Nombre_Univ TEXT sol_uni REFERENCES Universidades, Carrera TEXT NOT NULL, Decision BOOL, CONSTRAINT sol_PK PRIMARY KEY (id, Nombre_Univ, Carrera))")
    print ('Tabla "Solicitudes" creada con exito en ' + dbfile + '\n')

#apartado 2
def rellenarTablas(cur, conn):
    cur.executemany('INSERT INTO Universidades(Nombre_Univ, Comunidad, Plazas)VALUES( ?, ?, ?)', [( ' Universidad Complutense de Madrid', 'Madrid', 15000), (' Universidad de Barcelona', 'Barcelona', 36000), (' Universidad de Valencia', 'Valencia', 10000),(' UPM', 'Madrid', 21000)])
    conn.commit()
    print ('Tabla "Universidades" rellenada con exito en ' + dbfile)
    
    estudiantes = [(123, 'Antonio', 8.9, 1000), (234, 'Juan', 8.6,1500),(345, 'Isabel',8.5,500), (456,'Doris',7.9,1000),(543,'Pedro',5.4,2000),(567,'Eduardo',6.9,2000),(654,'Alfonso',7.9,1000),(678,'Carmen',5.8,1000),(765,'Javier',7.9,1500),(789,'Isidro',8.4,800),(876,'Irene',6.9,400),(987,'Elena',6.7,800)]
    for row in estudiantes:
        cur.execute('INSERT INTO Estudiantes VALUES (?, ?, ?, ?)',row)
    conn.commit()
    print ('Tabla "Estudiantes" rellenada con exito en ' + dbfile)
    
    solicitudes = [(123, 'Universidad Complutense de Madrid', 'Informatica', True),(123, 'Universidad Complutense de Madrid', 'Economia', False),
    (123, 'Universidad de Barcelona', 'Informatica', True), (123, 'UPM', 'Economia', True),
    (234, 'Universidad  de Barcelona', 'Biologia', False),(345, 'Universidad de Valencia', 'Bioingenieria', True),
    (345, 'UPM', 'Bioingenieria', False),(345, 'UPM', 'Informatica', True), (345, 'UPM', 'Economia', False),
    (678, 'Universidad Complutense de Madrid', 'Historia', True), (987, 'Universidad Complutense de Madrid', 'Informatica', True),
    (987, 'Universidad de Barcelona', 'Informatica', True), (876, 'Universidad Complutense de Madrid', 'Informatica', False),
    (876, 'Universidad de Valencia', 'Biologia', True), (876, 'Universidad de Valencia', 'Biologia Marina', False),
    (765, 'Universidad Complutense de Madrid', 'Historia', True), (765, 'UPM', 'Historia', False), (765, 'UPM', 'Psicologia', True),
    (543, 'Universidad de Valencia', 'Informatica', False)]
    for row2 in solicitudes:
        cur.execute('INSERT INTO Solicitudes VALUES (?, ?, ?, ?)',row2)
    print ('Tabla "Solicitudes" rellenada con exito en ' + dbfile + '\n')
    conn.commit()



if __name__ == '__main__':

    dbfile="Universidad.sqlite3"

    conn, cur = login(dbfile)
    crearTablas(cur)
    rellenarTablas(cur, conn)



    #CONSULTA 1
    print ('\n CONSULTA 1:')
    sel = cur.execute('SELECT DISTINCT e.Nombre_Est,e.Nota,s.Decision FROM Estudiantes e, Solicitudes s WHERE  e.Valor < 1000 AND s.Decision = (SELECT Decision from Solicitudes WHERE Nombre_Univ = "Universidad Complutense de Madrid" AND Carrera = "Informatica" AND e.id = id )')
    for (nombre, nota, dec) in sel.fetchall():
        print ('Nombre: ' + nombre)
        print ('Nota: ' + nombre)
        if (dec == 0):
           print ('Decision: No \n')
        else:
           print ('Decision: Si \n')
           
    #CONSULTA 2
    print ('\n CONSULTA 2:')
    idsel = cur.execute('SELECT id FROM Estudiantes WHERE ABS(((Nota*Valor)/1000)-Nota) > 1')
    for res in idsel.fetchall():
        print ('Id de estudiante' + str(res))
    print('\n')
    
    #CONSULTA 3
    print ('\n CONSULTA 3:')
    #primero anadimos la Universidad de Jaen a la tabla Universidades
    cur.execute('INSERT INTO Universidades(Nombre_Univ, Comunidad, Plazas)VALUES("Universidad de Jaen", "Jaen", 5000)')
    conn.commit()
    print ('"Universidad de Jaen" insertada en tabla "Universidades" con exito')
    IDS = cur.execute('SELECT id FROM Estudiantes WHERE NOT EXISTS(SELECT * FROM Solicitudes WHERE Estudiantes.id = Solicitudes.id)')
    for id in IDS.fetchall():
         cur.execute('INSERT INTO Solicitudes(id,Nombre_Univ,Carrera) VALUES (?,"Universidad de Jaen","Informatica")',id)
    conn.commit()
    print ('Tabla "Solicitudes" modificada con exito \n')


    #CONSULTA 4
    print ('\n CONSULTA 4:')
    ids2 = cur.execute ('SELECT DISTINCT id FROM Solicitudes WHERE Carrera = "Economia" AND Decision = 0')

    for id in ids2.fetchall():
        b=True
        for decision in cur.execute('SELECT Decision FROM Solicitudes WHERE Carrera = "Economia" AND ID = ?',id).fetchall():
            b= b and not(decision[0])

        if (b):
            cur.execute('INSERT INTO Solicitudes(id,Nombre_Univ,Carrera,Decision) VALUES (?,"Universidad de Jaen","Economia",1)', id )
    conn.commit()
    print ('Tabla "Solicitudes" modificada con exito \n')


    #CONSULTA 5
    print ('\n CONSULTA 5:')
    ids3 = cur.execute('SELECT COUNT(DISTINCT s.Carrera), e.id FROM Solicitudes s, Estudiantes e WHERE s.id = e.id GROUP BY s.id')
    for (Count, ide) in ids3.fetchall():
        if Count > 2:
            cur.execute('DELETE FROM Solicitudes WHERE id =?',[ide])
    conn.commit()
    print ('Tabla "Solicitudes" modificada con exito \n')

    cur.close()
