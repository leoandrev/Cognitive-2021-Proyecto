from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask import request
# Redireccionar
from flask import redirect, url_for, session
# Enviar mensajes entre vistas
from flask import flash
# import bcrypt
from dao.DAOe import Manager
from functions import *
from datetime import date

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'db_prueba1'

mysql = MySQL(app)

# Session Settings 
app.secret_key = 'mysecretkey'

# Semilla para encriptamiento
# semilla = bcrypt.gensalt()
Db = Manager()


# ------ RUTAS Y FUNCIONES ------ #
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def loginRequest():
    if request.method == 'POST':
        correo = request.form['correoh']
        contraseña = request.form['contrash']
        # Dar los datos a MySQL; Cursor para saber 
        # dónde está la conexión
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE correo=%s', (correo,))
        # Función para guardar en 'user' un elemento
        user = cur.fetchone()
        print(user)
        cur.close()

        if len(user) > 0: # Si existe el usuario
            if contraseña == user[3]:
                print('coinciden')
                #session['S_usuario'] = user[1]
                session['S_id'] = user[0]
                session['S_privilegio'] = user[4]
                if session['S_privilegio'] == 'admin':
                    return redirect(url_for('books')) 
                else:
                    return redirect(url_for('inicio'))
            else:
                flash("Error. La contraseña no es correcta.")
                return redirect(url_for('login'))
        else:
            flash("El usuario no existe.")
            return redirect(url_for('login'))

@app.route('/register')
def register():    
    return render_template("registrar.html")

@app.route('/registerRequest', methods=["POST"])
def registerRequest():
    if request.method == 'POST':
        usuario = request.form['usuarioh']
        correo = request.form['correoh']
        contraseña = request.form['contrash']
        ## session['user'] = correo
        # Dar los datos a MySQL; Cursor para saber 
        # dónde está la conexión
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (usuario, correo, contrasena, privilegio) VALUES (%s, %s, %s, "usuario")', 
        (usuario, correo, contraseña))
        # Función para ejecutar la consulta
        mysql.connection.commit()
        flash('Usuario registrado satisfactoriamente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('S_id', None)
    session.pop('S_privilegio', None)
    flash('Sesión cerrada.')
    return redirect(url_for('login'))



# ------ USUARIO ------ #
@app.route('/main')
def inicio():
    if 'S_id' in session:
        if session['S_privilegio'] == 'usuario':
            return redirect(url_for('UserBooks'))
        
        else:
            flash('Esta ruta corresponde a usuario.')
            return redirect(url_for('admin'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/books')
def UserBooks():
    if 'S_id' in session:
        if session['S_privilegio'] == 'usuario':
            # Traer libros prestados
            detalles, prestamos = User_get_Prestamos_y_detalles(session['S_id'], 0)
            print(detalles)
            Libros_pendientes = User_verLibros(detalles)
            print('TERMINADO')
            detalles, prestamos = User_get_Prestamos_y_detalles(session['S_id'], 1)
            Libros_mora = User_verLibros(detalles)
            # Traer préstamos con mora
            return render_template('indexusuario.html', Libros_pendientes=Libros_pendientes, Libros_mora=Libros_mora)
        else:
            flash('Esta ruta corresponde a usuario.')
            return redirect(url_for('admin'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/books/clearDebt')
def clearDebt():
    if 'S_id' in session:
        if session['S_privilegio'] == 'usuario':
            # Traer libros con mora
            #print('DETALLES')
            detalles, prestamos = User_get_Prestamos_y_detalles(session['S_id'], 1)
            #print('Ahora si')
            #print(detalles)
            Libros_mora = User_verLibros(detalles)
            #print('Libros mora:', Libros_mora)
            Libros_mora = list(Libros_mora)
            #print('Nuevo_ibros mora:', Libros_mora)
            # Traer préstamos con mora
            for i in range(len(Libros_mora)):
                print('Libro a ser eliminado:', Libros_mora[0])
                Db.delete_detallePrestamo(Libros_mora[i][0], 1)
            return redirect(url_for('UserBooks'))
        else:
            flash('Esta ruta corresponde a usuario.')
            return redirect(url_for('admin'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/books/return/<int:id>')
def giveBackBook(id):
    if 'S_id' in session:
        if session['S_privilegio'] == 'usuario':
            # Traer detallePrestamo asociado a idLibro y Usuario_idUsuario
            #idsPrestamo = Db.idPrestamo_From_Prestamo(id)
            detalles, prestamos = User_get_Prestamos_y_detalles(session["S_id"], 0)
            # print(detalles)
            for i in range(len(detalles)):
                idDetalle = Db.iddetallePrestamo_from_detallePrestamo(id)
            idDetalle = idDetalle[0]
            today = date.today()
            if Db.registrar_devolucion(today, idDetalle):
                flash('Libro devuelto :)')
            else:
                flash('Error al devolver el libro')
            
            return redirect(url_for('UserBooks'))
        else:
            flash('Esta ruta corresponde a usuario.')
            return redirect(url_for('admin'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

# ---------------------- #

# ------ ADMIN ------ #
@app.route('/admin')
def admin():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            books = Db.get_Libros(None)
            users = Db.get_Users(None)
            return render_template('index.html', data_books=books, data_users=users)
    
        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/books')
def books():
    if session['S_privilegio'] == 'admin':
        books = Db.get_Libros(None)
        print(books)
        users = Db.get_Users(None)
        return render_template('index.html', data_books=books, data_users=users)

    else:
        flash('No tienes autorización para ingresar a esta ruta.')
        return redirect(url_for('inicio'))

@app.route('/admin/books/add')
def addBook():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            category = Db.find_Category(None, None)
            print(category)
            return render_template('addbook.html', categories = category)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/books/addRequest', methods=["POST"])
def addBookRequest():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            if request.method == 'POST':
                nombre = request.form["nombre"]
                autor = request.form["autor"]
                anio = request.form["anio"]
                edicion = request.form["edicion"]
                ISBN = request.form["ISBN"]
                idCategoria = request.form["categoria"]
                print(idCategoria)
                #idCategoria = Db.findCategory(categoria, None)
                #idCategoria = idCategoria[0]
                data = [nombre, autor, anio, edicion, ISBN, idCategoria]
                print(data)
                
                if Db.insert_Book(data):
                    flash('Libro añadido :)')
                    return redirect(url_for('admin'))
                else:
                    flash('Inserción fallida. Vuelva a intentar')
                    return redirect(url_for('admin'))
        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/books/update/<int:id>')
def updateBook(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':            
            book = Db.get_Libros(id)
            libro = book[0]
            id = int(libro[7])
            category = Db.find_Category(None, id)
            category = category[0]
            # print(book)
            return render_template('update.html', book = book, category=category)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/books/updateRequest/<int:id>', methods=['POST'])
def updateBookRequest(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            if request.method == 'POST':
                nombre = request.form['nombre']
                print(nombre)
                autor = request.form["autor"]
                anio = request.form["anio"]
                edicion = request.form["edicion"]
                ISBN = request.form["ISBN"]
                categoria = request.form["categoria"]

                idCategoria = Db.findCategory(categoria, None)
                idCategoria = (idCategoria[0])[0]
                data = [nombre, autor, anio, edicion, ISBN, idCategoria, id]
                
                if Db.updateBook(data):
                    flash('Libro actualizado :)')
                    return redirect(url_for('admin'))
                else:
                    flash('Actualización fallida. Vuelva a intentar')
                    return redirect(url_for('admin'))

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))


@app.route('/admin/books/delete/<int:id>')
def deleteBookRequest(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':            
            book = Db.get_Libros(id)
            libro = book[0]
            id = int(libro[7])
            category = Db.find_Category(None, id)
            category = category[0]
            return render_template('update.html', books = book, category=category)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/books/deleteRequest/<int:id>') #HECHA
def deleteBook(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            ids_detallePrestamo = Db.iddetallePrestamo_from_detallePrestamo(id)
            # print('IDs de detallePrestamo:', ids_detallePrestamo)
            # ID's de detallePrestamo: ((12,), (15,))
            if len(ids_detallePrestamo) > 0:
                flash('No puede eliminarse el libro. Hay préstamos asociados.')
                return redirect(url_for('books'))
            else:
                Db.deleteBook(id)
                flash('Operacion hecha.')
                return redirect(url_for('books'))            

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))


@app.route('/admin/users')
def Users():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            data = Db.get_Users(None)            
            return render_template('admin/users.html', data_usuarios=data)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
            

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))


@app.route('/admin/users/<int:id>')
def User(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            data = Db.get_Users(id)
            detalles, prestamos = User_get_Prestamos_y_detalles(id, 1)
            Libros_mora = User_verLibros(detalles)
            return render_template('checkuser.html', data_usuario=data, Libros_mora=Libros_mora)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/users/add')
def addUser():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            return render_template('addusuario.html')

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/users/addRequest', methods=["POST"])
def addUserRequest():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            if request.method == 'POST':
                email = request.form["email"]
                username = request.form["username"]
                password = request.form["password"]
                privilegio = request.form["privilegio"]
                data = [email, username, password, privilegio]

                if Db.insert_User(data):
                    flash('Usuario agregado :)')
                else:
                    flash('Error al agregar usuario.')
                return redirect(url_for('addUser'))

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/users/delete/<int:id>') # LISTA PARA PROBARSE
def deleteUserRequest(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            detalles, prestamos = User_get_Prestamos_y_detalles(id, None)
            detalles = list(detalles)
            prestamos = list(prestamos)
            print('IDs de detallePrestamos asociados al usuario:',detalles)
            print('IDs de Prestamos asociados al usuario:',prestamos)
            # Eliminacion de detallePrestamo
            if len(prestamos) > 0:
                for i in range(len(prestamos)):
                    Db.delete_detallePrestamo(prestamos[i], 0)
            # Eliminacion de Prestamos
            Db.delete_Prestamo(id)
            
            # Eliminacion de Usuario
            Db.delete_User(id)
            flash('Operación ejecutada.')

            return redirect(url_for('books'))

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

# ------------------- #

if __name__ == '__main__':
    app.run(port=3000, debug=True)

# ------------------------------- #
