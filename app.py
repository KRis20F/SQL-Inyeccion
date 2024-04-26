# -*- coding: utf-8 -*-
"""
Created on February 2023

@author: Albert ETPX
"""
# Importación de módulos externos
import mysql.connector
from flask import Flask,render_template,request;

# Funciones de backend #############################################################################

# connectBD: conecta a la base de datos users en MySQL
def connectBD():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "users"
    )
    return db

# initBD: crea una tabla en la BD users, con un registro, si está vacía
def initBD():
    bd=connectBD()
    cursor=bd.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS users;")
    # Operación de creación de la tabla users (si no existe en BD)
    query="CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            genre enum('H','D','NS/NC')); "
    cursor.execute(query)
            
    # Operación de inicialización de la tabla users (si está vacía)
    query="SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if(count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Ramón','Sigüenza','López',35,'H');"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return

# checkUser: comprueba si el par usuario-contraseña existe en la BD
def checkUser(user,password):
    bd=connectBD()
    cursor=bd.cursor()
    query="SELECT user,name,surname1,surname2,age,genre FROM users WHERE user= %s AND password = %s" #He creado esta parte
    values = (user, password)
    print(query)
    cursor.execute(query, values)
    userData = cursor.fetchall()
    bd.close()
    
    if userData == []:
        return False
    else:
        return userData[0]
    
# cresteUser: crea un nuevo usuario en la BD
def createUser(usuario,newPasswd,newNom,newCognom,newCognom2,newEdad,newGenero):
    bd=connectBD()
    cursor = bd.cursor()
    query = "INSERT INTO users (user, password, name, surname1, surname2, age, genre) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = usuario, newPasswd,newNom,newCognom,newCognom2,newEdad,newGenero
    cursor.execute(query, values)
    bd.commit()
    bd.close()
    
# CREACION DE NUEVO USUARIO POR MI

# Secuencia principal: configuración de la aplicación web ##########################################
# Instanciación de la aplicación web Flask
app = Flask(__name__)

# Declaración de rutas de la aplicación web
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    initBD()
    return render_template("login.html")

@app.route("/signin.html")
def signin():
    initBD()
    return render_template("signin.html")

# CODIGO HECHO
@app.route("/registre", methods = ('GET', 'POST'))
def registre():
    if request.method == ('POST'):
        formData = request.form
        newuser = formData['usuario']
        newPasswd = formData['contraseña']
        newNom = formData['nombre']
        newCognom = formData['apellido']
        newCognom2 = formData['apellido2']
        newEdad = formData['edad']
        newGenere = formData['genero'] 
        createUser(newuser,newPasswd,newNom,newCognom,newCognom2,newEdad,newGenere)
        return render_template("home.html")  
    else:
        return "NADA"
     
#FIN DEL CODIGO HECHO PARA EL FORMULARIO DEL REGISTRO 
@app.route("/results",methods=('GET', 'POST'))
def results():
    if request.method == ('POST'):
        formData = request.form
        user=formData['usuario']
        password=formData['contrasena']
        userData = checkUser(user,password)

        if userData == False:
            return render_template("results.html",login=False)
        else:
            return render_template("results.html",login=True,userData=userData)
        
# Configuración y arranque de la aplicación web
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)