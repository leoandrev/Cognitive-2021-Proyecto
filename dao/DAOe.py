import pymysql

class Manager:
    def connect(self):
        return pymysql.connect(host="localhost",user="root",password="",db="db_prueba1")

    def get_Users(self, id):
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

    def insert_User(self, data, confirmacion): #AQUI FALTA
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

    def delete_User(self, id): # AQUI FALTA
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

    def get_Prestamo(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM prestamo where Usuario_idUsuario = %s", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def get_Libros(self, id): # FALTA PARA EL USUARIO. PARA EL ADMIN ESTA LISTO
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

    def insert_Book(self, data): # AQUI FALTA
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO libro(nombre, autor, anio, edicion, ISBN, Categoria_idCategoria) VALUES(%s, %s, %s, %s, %s, %s)", (data['nombre'], data["autor"], data['anio'], data['edicion'], data['ISBN'], data['idCategoria'], ))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def find_Category(self, categoria, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if categoria == None:
                cursor.execute("SELECT nombre FROM Categoria where idCategoria = %s", (id, ))
            if id == None:
                cursor.execute("SELECT idCategoria FROM Categoria where nombre = %s", (categoria, ))
            if categoria == None and id == None:
                cursor.execute("SELECT idCategoria, nombre FROM Categoria")
            return cursor.fetchall()

        except:
            return ()
        
        finally:
            con.close()

    def idPrestamo_From_Prestamo(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT idPrestamo FROM Prestamo where Usuario_idUsuario = %s", (id,) )
            return cursor.fetchall()

        except:
            return ()
        
        finally:
            con.close()

    def Prestamo_pendiente(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT Prestamo_idPrestamo FROM detallePrestamo where Libro_idLibro = %s && fecha_devolucion > fecha_entrega", (id,) )
            return cursor.fetchall()

        except:
            return ()
        
        finally:
            con.close()

    def idLibro_From_detallePrestamo(self, id, consulta):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if consulta == None:
                cursor.execute("SELECT Libro_idLibro FROM detallePrestamo where Prestamo_idPrestamo = %s", (id,) )
            else:
                if consulta == 0:
                    cursor.execute("SELECT Libro_idLibro FROM detallePrestamo where Prestamo_idPrestamo = %s && fecha_devolucion is NULL", (id,) )
                else:
                    cursor.execute("SELECT Libro_idLibro FROM detallePrestamo where Prestamo_idPrestamo = %s && fecha_devolucion > fecha_entrega", (id,) )
            
            return cursor.fetchall()
        except:
            return ()
        
        finally:
            con.close()

    def delete_detallePrestamo(self, id, indi):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if indi == 0:
                cursor.execute("DELETE FROM detallePrestamo where Prestamo_idPrestamo = %s", (id,))
            else:
                cursor.execute("DELETE FROM detallePrestamo where Libro_idLibro = %s", (id,))
            con.commit()
        except:
            con.rollback()
        finally:
            con.close()

    def delete_Prestamo(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM Prestamo where Usuario_idUsuario = %s", (id,))
            con.commit()
        except:
            con.rollback()
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

    def iddetallePrestamo_from_detallePrestamo(self, id):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT id_detallePrestamo FROM detallePrestamo where Libro_idLibro = %s", (id,) )
            return cursor.fetchall()
        except:
            return ()
        
        finally:
            con.close()

    def giveBack_Book(self, idLibro, idPrestamo):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT id_detallePrestamo FROM detallePrestamo where Libro_idLibro = %s && Prestamo_idPrestamo = %s", (idLibro, idPrestamo, ) )
            return cursor.fetchall()
        except:
            return ()
        
        finally:
            con.close()

    def registrar_devolucion(self, fecha, id_detallePrestamo):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE detallePrestamo set fecha_devolucion = %s where id_detallePrestamo = %s", (fecha, id_detallePrestamo, ))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def set_penalidad(self, penalidad, idUsuario):
        con = Manager.connect(self)
        cursor = con.cursor()

        try:
            if penalidad == 1:
                cursor.execute("UPDATE Usuario set habilitado = 0 where idUsuario = %s", (idUsuario,))
                con.commit()
            else:
                cursor.execute("UPDATE Usuario set habilitado = 1 where idUsuario = %s", (idUsuario,))
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