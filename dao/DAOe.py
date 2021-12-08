import pymysql

class Manager:
    def connect(self):
        return pymysql.connect(host="localhost",user="root",password="",db="db_prueba1")

    def readUsers(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM usuario where privilegio = 'usuario' order by correo asc")
            else:
                cursor.execute("SELECT * FROM usuario where id = %s && privilegio = 'usuario'", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close() # Se cierra la conexion en caso de error abrupto

    def insertUser(self, data, confirmacion): #AQUI FALTA
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if confirmacion == 1:
                cursor.execute("INSERT INTO usuario(correo, nickname, contrasena, privilegio) VALUES(%s, %s, %s, 'usuario')", (data['correo'],data['nickname'],data['contrasena'],))
                con.commit()
                return True
            else:
                cursor.execute("INSERT INTO usuario(correo, nickname, contrasena, privilegio) VALUES(%s, %s, %s, 'admin')", (data['correo'], data['nickname'],data['contrasena'],))
                con.commit()
                return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def deleteUser(self, id): # AQUI FALTA
        con = Manager.connect(self)
        cursor = con.cursor()        

        try:
            cursor.execute("DELETE FROM usuario where id = %s", (id,))
            cursor.execute("DELETE FROM prestamo where Usuario_idUsuario = %s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def readPrestamo(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM prestamo where Usuario_idUsuario = %s", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()    

    def readBooks(self, id): # FALTA PARA EL USUARIO. PARA EL ADMIN ESTA LISTO
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM libro order by nombre asc")
            else:
                cursor.execute("SELECT * FROM libro where idLibro = %s", (id,))
            return cursor.fetchall()
            
        except:
            return ()
        finally:
            con.close() # Se cierra la conexion en caso de error abrupto

    def insertBook(self, data): # AQUI FALTA
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO libro(nombre, autor, anio, edicion, ISBN) VALUES(%s, %s, %s, %s, %s)", (data['nombre'], data["autor"], data['anio'], data['edicion'], data['ISBN'],))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def findCategory(self, categoria, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if categoria == None:
                cursor.execute("SELECT nombre FROM Categoria where idCategoria = %s", (id, ))
            if id == None:
                cursor.execute("SELECT idCategoria FROM Categoria where nombre = %s", (categoria, ))
            return cursor.fetchall()

        except:
            return ()
        
        finally:
            con.close()

    def finddetallePrestamo(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT devuelto FROM detallePrestamo where Libro_idLibro = %s", (id, ))
            return cursor.fetchall()

        except:
            return ()
        
        finally:
            con.close()

    def deleteBook(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM libro where idLibro = %s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def updateBook(self, data):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE libro set nombre = %s, autor = %s, anio = %s, edicion = %s, ISBN = %s, Categoria_idCategoria = %s where idLibro = %s", (data[0],data[1],data[2],data[3],data[4],data[5],data[6],))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()