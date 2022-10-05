import sqlite3
from flask import Flask, jsonify, render_template, request, url_for, redirect,session
from flask_session import Session
import json

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = 'clave-oculta'


@app.route('/')
def index():
    return render_template ('home.html')

def buscarUsuario(user, password):
    conn = sqlite3.connect('memotest2.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT *
                      FROM Jugadores
                      WHERE nombre = '{user}'AND contraseña = '{password}';
                  """)
    user = cur.fetchall()
    conn.commit()
    conn.close()
    if user != []:
      return "True"
    else:
      return "False"


@app.route('/log', methods=['POST'])
def log():

  session['nombre'] = request.form['nombre']
  session['contra'] = request.form['contra']
  session['admin'] = False
  if buscarUsuario(session['nombre'],session['contra']) == "True":
    if session['nombre']=='admin' and session['contra']=='admin':
      session['admin'] = True
    print(session['admin'])
    return "True"
  else:
    return "El usuario no existe"



@app.route('/register', methods=['POST'])
def register():
  nombre = request.form['nombre']
  contra = request.form['contra']
  if buscarUsuario(nombre,contra) == "True":
    return "Usuario en uso"
  else:
    con = sqlite3.connect('memotest2.db')
    q = f"""INSERT INTO Jugadores (nombre,contraseña) VALUES ('{nombre}', '{contra}')"""
    con.execute(q)
    con.commit()
    con.close()
    return 'True'

@app.route('/inicio')
def logeado():
  return render_template('iniciado.html')

@app.route('/tablero/<id>')
def tablero(id):
  conn = sqlite3.connect('memotest2.db')
  cur = conn.cursor()
  cur.execute(f"""SELECT valor
                  FROM Tableros
                  WHERE idTablero = {id} AND numerofila = 0
                  ORDER BY numeroFila ASC, numeroColumna ASC;""")
  valores1 = cur.fetchall()
  
  cur.execute(f"""SELECT valor
                  FROM Tableros
                  WHERE idTablero = {id} AND numerofila = 1
                  ORDER BY numeroFila ASC, numeroColumna ASC;""")
  valores2 = cur.fetchall()
  
  cur.execute(f"""SELECT numeroFila
                  FROM Tableros
                  WHERE idTablero = {id}
                  GROUP BY numeroFila;""")  
  filas = cur.fetchall()
  valores = [valores1, valores2]
  cantFilas = []

  for a in range (len(filas)):
    print(a)
    fila = []
    value = valores[a]
    print(value)
    for i in range (len(value)):
      fila.append(value[i])

    cantFilas.append(fila)

  
  conn.close()
  print(cantFilas)
  admin = True
  return render_template ('base_tableros.html', admin = admin, cantFilas = cantFilas)

app.run(host='0.0.0.0', port=81)
