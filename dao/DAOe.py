import pymysql

class DAOUsuario:
    def connect(self):
        return pymysql.connect(host="localhost",user="root",password="",db="db_poo" )

    def update(self, id, data):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE usuario set nombre = %s, telefono = %s, email = %s where id = %s", (data['nombre'],data['telefono'],data['email'],id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()


class Manager:
    def connect(self):
        return pymysql.connect(host="localhost",user="root",password="",db="db_prueba1")

    def readUsers(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM usuario where privilegio = 'usuario' order by nombre asc")
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
                cursor.execute("SELECT * FROM libro where id = %s order by nombre asc", (id,))
            return cursor.fetchall()
            
        except:
            return ()
        finally:
            con.close() # Se cierra la conexion en caso de error abrupto

    def insertBook(self, data): # AQUI FALTA
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO libro(nombre, anio, edicion, ISBN) VALUES(%s, %s, %s, %s)", (data['nombre'], data['anio'], data['edicion'], data['ISBN'],))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def deleteBook(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM libro where id = %s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update(self, id, data):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE usuario set nombre = %s, telefono = %s, email = %s where id = %s", (data['nombre'],data['telefono'],data['email'],id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()