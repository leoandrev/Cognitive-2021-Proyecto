from flask import Flask, render_template
from flask_mysqldb import MySQL, MySQLdb
from flask import request
# Redireccionar
from flask import redirect, url_for, session
# Enviar mensajes entre vistas
from flask import flash
# import bcrypt

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bibliotecaApp'

mysql = MySQL(app)

# Session Settings 
app.secret_key = 'mysecretkey'

# Semilla para encriptamiento
# semilla = bcrypt.gensalt()


# ------ RUTAS Y FUNCIONES ------ #
@app.route("/")
def login():
    return render_template('login.html')
    

@app.route("/loginusuario", methods=["POST"])
def loginusuario():
    if request.method == 'POST':
        correo = request.form['correoh']
        contraseña = request.form['contrash']
        print(contraseña)
        ## session['user'] = correo
        # Dar los datos a MySQL; Cursor para saber 
        # dónde está la conexión
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo=%s', (correo,))
        # Función para guardar en 'user' un elemento
        user = cur.fetchone()
        user1 = cur.fetchall()
        print(user)
        print(user1)
        cur.close()

        if len(user) > 0: # Si existe el usuario
            if contraseña == user[3]:
                print('coinciden')
                session['S_usuario'] = user[1]
                session['S_id'] = user[0]
                session['S_privilegio'] = user[4]
                return redirect(url_for('inicio'))
            else:
                flash("Error. La contraseña no es correcta.")
                return redirect(url_for('login'))
        else:
            flash("El usuario no existe.")
            return redirect(url_for('login'))
        
    else:
        return render_template('login.html')

@app.route("/register")
def registrar():
    return render_template("registrar.html")

@app.route("/registerusuario", methods=["POST"])
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

@app.route("/inicio")
def inicio():
    if 'S_usuario' in session:
        if session['S_privilegio'] == 'usuario':
            return render_template('inicio.html')
        else:
            return render_template('dashboard.html')
    else:
        flash('No has iniciado sesión aún.')
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('S_usuario', None)
    session.pop('S_privilegio', None)
    flash('Sesión cerrada.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)

# ------ USUARIO ------#


# ------ ADMIN ------ #
@app.route('/dahsboard')
def principal_dashboard():
    if session['S_privilegio'] == 'usuario':
        return render_template('<h1> No tienes autorización para entrar aquí</h1>')
    
    else:

        return render_template('admin/dashboard.html')

@app.route('/dashboard/books')
def books():
    return 
    

# ------------------- #

# ------------------------------- #
