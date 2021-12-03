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
app.config['MYSQL_DB'] = 'db_prueba'

mysql = MySQL(app)

# Session Settings 
app.secret_key = 'mysecretkey'

# Semilla para encriptamiento
# semilla = bcrypt.gensalt()
Handler = Manager()


# ------ RUTAS Y FUNCIONES ------ #
@app.route('/')
def login():
    return render_template('login.html')
    

@app.route('/loginusuario', methods=["POST"])
def loginusuario():
    if request.method == 'POST':
        correo = request.form['correoh']
        contraseña = request.form['contrash']
        ## session['user'] = correo
        # Dar los datos a MySQL; Cursor para saber 
        # dónde está la conexión
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE nickname=%s', (correo,))
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
                    return redirect(url_for('admin')) #"<h1> Accediste como admin </h1>" #
                #else:
                    #return render_template('inicio.html')
            #else:
            flash("Error. La contraseña no es correcta.")
            return redirect(url_for('login'))
        else:
            flash("El usuario no existe.")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')

@app.route('/register')
def registrar():
    return render_template("registrar.html")

@app.route('/registerusuario', methods=["POST"])
def registrar_usuario():
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
@app.route('/inicio')
def inicio():
    if 'S_id' in session:
        if session['S_privilegio'] == 'usuario':
            return render_template('inicio.html')
        else:
            flash('Esta ruta corresponde a usuario.')
    else:
        flash('No has iniciado sesión aún.')
        return render_template('login.html')


# ---------------------- #

# ------ ADMIN ------ #
@app.route('/admin')
def admin():
    #if session['S_privilegio'] == 'admin':
        return render_template('dashboard.html')
    
    #else:
        #flash('No tienes autorización para ingresar a esta ruta.')
        #return render_template('inicio.html')
        

@app.route('/admin/books')
def books():
    if session['S_privilegio'] == 'admin':
        books = Handler.readBooks(None)
        print(books)
        return render_template('index.html', data_books=books)

    else:
        flash('No tienes autorización para ingresar a esta ruta.')
        return render_template('inicio.html')
        
    
    
@app.route('/admin/users')
def ViewUsers():
    if session['S_privilegio'] == 'usuario':
        flash('No tienes autorización para ingresar a esta ruta.')
        return render_template('admin/dashboard.html')

    else:
        data = Handler.readUsers(None)
        return render_template('admin/users.html', data_usuarios=data)


@app.route('/admin/users/<int:id>')
def ViewSingleUser(id):
    if session['S_privilegio'] == 'usuario':
        flash('No tienes autorización para ingresar a esta ruta.')
        return render_template('admin/dashboard.html')

    else:
        user = Handler.readUsers(id)
        return render_template('admin/user.html', data_usuario = user)


# ------------------- #

if __name__ == '__main__':
    app.run(port=3000, debug=True)

# ------------------------------- #
