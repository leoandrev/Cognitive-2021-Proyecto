from re import A
from flask import Flask, render_template
from flask_mysqldb import MySQL, MySQLdb
from flask import request
# Redireccionar
from flask import redirect, url_for, session
# Enviar mensajes entre vistas
from flask import flash
# import bcrypt
from dao.DAOe import Manager

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_prueba1'

mysql = MySQL(app)

# Session Settings 
app.secret_key = 'mysecretkey'

# Semilla para encriptamiento
# semilla = bcrypt.gensalt()
Handler = Manager()


# ------ RUTAS Y FUNCIONES ------ #
@app.route('/', methods=["POST"])
def login():
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
                    return redirect(url_for('admin')) 
                else:
                    return redirect(url_for('inicio'))
            else:
                flash("Error. La contraseña no es correcta.")
                return redirect(url_for('login'))
        else:
            flash("El usuario no existe.")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')

@app.route('/register', methods=["POST"])
def registrar():
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
    return render_template("registrar.html")
    

@app.route('/logout')
def logout():
    session.pop('S_id', None)
    session.pop('S_privilegio', None)
    flash('Sesión cerrada.')
    return redirect(url_for('login'))



# ------ USUARIO ------ #
@app.route('/inicio')
def inicio():
    if 'S_id' in session:
        if session['S_privilegio'] == 'usuario':
            return render_template('inicio.html')
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
            books = Handler.readBooks(None)
            users = Handler.readUsers(None)
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
        books = Handler.readBooks(None)
        print(books)
        return render_template('index.html', data_books=books)

    else:
        flash('No tienes autorización para ingresar a esta ruta.')
        return render_template('inicio.html')

@app.route('/admin/books/add')
def addBook():
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            if request.method == 'POST':
                nombre = request.method["nombre"]
                autor = request.method["autor"]
                anio = request.method["anio"]
                edicion = request.method["edicion"]
                ISBN = request.method["ISBN"]
                categoria = request.method["categoria"]
                idCategoria = Handler.findCategory(categoria, None)
                idCategoria = idCategoria[0]
                data = [nombre, autor, anio, edicion, ISBN, idCategoria]
                
                if Handler.insertBook(data):
                    flash('Libro añadido :)')
                    return redirect(url_for('admin'))
                else:
                    flash('Inserción fallida. Vuelva a intentar')
                    return redirect(url_for('addBook'))

            return render_template('agregarlibro.html')

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return render_template('inicio.html')
    
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))

@app.route('/admin/books/update/<int:id>', methods=['POST'])
def bookaddRequest(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            if request.method == 'POST':
                id = id
                nombre = request.form['nombre']
                print(nombre)
                autor = request.form["autor"]
                anio = request.form["anio"]
                edicion = request.form["edicion"]
                ISBN = request.form["ISBN"]
                categoria = request.form["categoria"]
                idCategoria = Handler.findCategory(categoria, None)
                idCategoria = idCategoria[0]
                idCategoria = idCategoria[0]
                data = [nombre, autor, anio, edicion, ISBN, idCategoria, id]
                
                if Handler.updateBook(data):
                    flash('Libro actualizado :)')
                    return redirect(url_for('admin'))
                else:
                    flash('Actualización fallida. Vuelva a intentar')
                    return redirect(url_for('admin'))

            # En caso el método no sea POST
            book = Handler.readBooks(id)
            libro = book[0]
            id = int(libro[7])
            category = Handler.findCategory(None, id)
            category = category[0]
            return render_template('update.html', books = book, category=category)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return redirect(url_for('inicio'))
    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))


@app.route('/admin/books/delete/<int:id>')
def deleteBook(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            if request.method == 'POST':
                id = request.form["id"]
                detalle = Handler.finddetallePrestamo(id)
                if len(detalle) != 0:
                    flash('Operación fallida. Hay préstamos pendientes.')
                else:
                    if Handler.deleteBook(id):
                        flash('Operación exitosa')
                    else:
                        flash('Operación fallida. Vuelva a intentar.')
                
                return redirect(url_for('books'))
                    
            # En caso el método no sea POST
            book = Handler.readBooks(id)
            libro = book[0]
            id = int(libro[7])
            category = Handler.findCategory(None, id)
            category = category[0]
            return render_template('update.html', books = book, category=category)

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
            data = Handler.readUsers(None)            
            return render_template('admin/users.html', data_usuarios=data)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return render_template('admin/dashboard.html')
            

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))


@app.route('/admin/users/<int:id>')
def User(id):
    if 'S_privilegio' in session:
        if session['S_privilegio'] == 'admin':
            data = Handler.readUsers(id)            
            # prestamos = Hanlder.
            return render_template('admin/users.html', data_usuario=data)

        else:
            flash('No tienes autorización para ingresar a esta ruta.')
            return render_template('admin/dashboard.html')
            

    else:
        flash('No has iniciado sesión aún.')
        return redirect(url_for('login'))


# ------------------- #

if __name__ == '__main__':
    app.run(port=3000, debug=True)

# ------------------------------- #
