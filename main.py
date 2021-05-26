from flask import Flask, render_template,request,url_for,redirect,session,flash
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

#MySql connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'festtiva'

mysql = MySQL(app)

#Session
app.secret_key = 'fesstiva'

#hash encriptamiento
hash = bcrypt.gensalt()

#Funcion para saber si esta autenticado
def estaAutenticado():
    #Si esta autenticado podra navegar en la pagina de inicio
    if 'nombre' in session:
        #carga template de usuario logueado
        return render_template('main_page.html')
    else:
        #carga template de login si no esta autenticado
        return render_template('login.html')


#Definimos la ruta principal
@app.route("/")
def Index():
    return estaAutenticado()

#Ruta y funcion para agregar nuevo usuario
@app.route("/add_user", methods =['POST'])
def addContact():
 if request.method == 'POST':

   username = request.form['username']
   email = request.form['email']
   password = request.form['pass']
   password_encode = password.encode('utf-8')
   #encriptamos la contraseña utilizando la libreria
   password_encriptado =  bcrypt.hashpw(password_encode,hash)
   cur = mysql.connection.cursor()
   try:
    cur.execute('INSERT INTO usuarios (username,email,password) VALUES(%s, %s, %s)',(username,email,password_encriptado))
    mysql.connection.commit()
    flash('CONTACT ADDED SUCCESFULLY!!',"success")
   except Exception:
    flash('This user already exist','error')
    return render_template("registro.html")
   #Una vez creado el nuevo usuario redirigimos a la funcion Index
   return redirect(url_for('Index'))

#Ruta y funcion para cerrar la sesion del usuario
@app.route('/closeSession')
def closeSession():
    session.clear()
    return redirect(url_for('Index'))

#Ruta y funcion para hacer login
@app.route('/sign_in',methods= ['POST'])
def sign_in():
    username = request.form['username']
    password = request.form['pass']
    password_encode = password.encode('utf-8')

    cur = mysql.connection.cursor()
    #Obtenemos la data del usuario que se quiere loguear
    cur.execute("select * from usuarios where username=%s",[username])
    usuario = cur.fetchone()
    #return {'USUARIO':usuario}  
    cur.close  
    if(usuario != None):
        password_encriptado_encode = usuario[3].encode()
        if bcrypt.checkpw(password_encode,password_encriptado_encode):

            session['nombre'] = usuario[2]
            flash('Logged!!','success')
            return estaAutenticado()
        else:
            flash('INCORRECT DATA','error')
            return estaAutenticado()
        
    return redirect(url_for('Index'))

#Eliminar usuario
@app.route("/delete/<string:id>",methods =['GET'])
def delete(id):
    if request.method == 'GET':
      idcontact = id
      cur = mysql.connection.cursor()
      cur.execute('DELETE FROM usuarios where id = {0}'.format(id))
      mysql.connection.commit()
      flash('CONTACT REMOVED SUCCESFULLY',"success")
      return redirect(url_for('Index'))

#Editar usuario aun no se implementa la vista
@app.route('/edit/<id>', methods = ['GET'])
def get_contact(id):
    if request.method == 'GET':
        id_contact = id
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE id = %s',[id])
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('edit_contact.html', contact = data[0])

#Actualizar usuario
@app.route('/update/<id>',methods = ['POST'])
def update(id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        id_contact = id
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s,phone = %s,email = %s where id = %s',(fullname,phone,email,id_contact))
        mysql.connection.commit()
        flash('CONTACT UPDATED SUCCESFULLY',"success")
        return redirect(url_for('Index'))

@app.route('/vistaRegistro')
def mostrarVistaRegistro():
    return render_template('registro.html')

if __name__ == '__main__':
 app.run(port = 3000, debug = True)



