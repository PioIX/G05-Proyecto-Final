import sqlite3
import random
from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from flask_session import Session
import json
from flask_socketio import SocketIO, join_room, leave_room, emit
import sqlite3, random

#from flask_sock import Sock

app = Flask(__name__)
app.secret_key = "Encriptar"
socketio = SocketIO(app, logger=True, engineio_logger=True)


mazo = []

class Carta:
  def __init__(self,valor, numero, palo, url):
    self.valor = valor
    self.numero = numero
    self.palo = palo
    self.url = url



@app.route("/")
def index():
  session['ronda'] = 0
  return render_template("home.html")

def buscarUsuario(user, password):
    conn = sqlite3.connect('truco.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT *
                      FROM Usuarios
                      WHERE usuario = '{user}'AND contraseña = '{password}';
                  """)
    user = cur.fetchall()
    conn.commit()
    conn.close()
    if user != []:
      return "True"
    else:
      return "False"

@app.route('/register', methods=['POST'])
def register():
  nombre = request.form['nombre']
  contra = request.form['contra']
  if buscarUsuario(nombre, contra) == "True":
    return "Usuario en uso"
  else:
    print("ola")
    con = sqlite3.connect('truco.db')
    q = f"""INSERT INTO Usuarios (usuario, contraseña) VALUES ('{nombre}', '{contra}')"""
    con.execute(q)
    con.commit()
    con.close()
    print("la")
    return 'True'


@app.route("/iniciado", methods=["GET", "POST"])
def mesas():
  print("HOLA")
  if request.method == "POST":
    session['nombre'] = request.form["nombre"]
    session['contra'] = request.form["contra"]
    if buscarUsuario(session['nombre'], session['contra']) == "True":
      print(session['contra'])
      if session['nombre'] == "admin" and session['contra'] == "admin":
        session['admin'] = True
      else:
        session['admin'] = False
      print(session['admin'])
      return 'True'
    else:
      return 'False'

@app.route("/iniciado2", methods=["GET", "POST"])
def mesas2():
  print("HOLA")
  if request.method == "POST":
    conn = sqlite3.connect("truco.db")
    id = request.form["id"]
    contra = request.form["contra"]
    x = f"""SELECT contraseña FROM Salas WHERE Id= '{id}'"""
    psw = conn.execute(x)
    if contra == psw:
      return True
    else:
      return False
      
    
    
    if buscarUsuario(session['nombre'], session['contra']) == "True":
      print(session['contra'])
      if session['nombre'] == "admin" and session['contra'] == "admin":
        session['admin'] = True
      else:
        session['admin'] = False
      print(session['admin'])
      return 'True'
    else:
      return 'False'

@app.route("/salaDeEspera/", methods=["GET"])
def esperar():
  if request.method == "GET":
    admin = session["admin"]
    conn = sqlite3.connect("truco.db")                                
    agarrar = """SELECT Id, roomname, contraseña FROM Sala WHERE Llena = ('No')"""
    salas = conn.execute(agarrar).fetchall()
    conn.close()
    print("a")
    return render_template("mesas.html", cantMesas = salas, admin = admin)

@app.route("/reglas")
def reglamento():
    return render_template("reglas.html")

@app.route("/crear")
def irACrear():
  conn = sqlite3.connect("truco.db")
  select = """SELECT MAX(Id) FROM Sala"""
  x = conn.execute(select).fetchall()
  id = x[0][0] + 1
  return render_template("crearMesa.html", id = id )
    
@app.route("/crearMesa", methods=["GET", "POST"])
def creacion():
  if request.method == "POST":
    puntos = request.form["puntos"]
    contra = request.form["contra"]
    roomname = request.form["nombre"]
    conn = sqlite3.connect("truco.db")
    crear = f"""INSERT INTO Sala (Llena, a30, roomname, contraseña) VALUES ('No', '{puntos}', '{roomname}', '{contra}')"""
    conn.execute(crear)
    conn.commit()
    conn.close()
    print("hola")
    return 'True'
    

@app.route("/aEsperar/", methods=["GET", "POST"])
def espera():
  if request.method == "GET":
    conn = sqlite3.connect("truco.db")
    x = """SELECT MAX(Id) FROM Sala"""
    ID = conn.execute(x).fetchone()[0]
    y = f"""SELECT roomname FROM Sala WHERE Id = {ID}"""
    name = conn.execute(y).fetchone()[0]
    z = f"""SELECT a30 FROM Sala WHERE Id = {ID}"""
    k = conn.execute(z).fetchone()[0]
    if k == "Si":
      points = 30
    else:
      points = 15
    return render_template("espera.html", id = ID, nombre = name, puntos =   points)
  else:
    return render_template("crearMesa.html")

@app.route("/eliminarMesa", methods=["GET", "DELETE"])
def eliminacion():
  if request.method == "DELETE":
    id = request.form['id']
    conn = sqlite3.connect("truco.db")
    eliminar = f"""DELETE FROM Sala WHERE Id = {id}"""
    conn.execute(eliminar)
    conn.commit()
    conn.close()
    print("hola")
    return 'True'
  else:
    return render_template("espera.html")

@app.route("/eliminarUsuario", methods=["GET", "DELETE"])
def eliminationation():
    id = request.form['id']
    conn = sqlite3.connect("truco.db")
    eliminar = f"""DELETE FROM Usuarios WHERE Id = {id}"""
    conn.execute(eliminar)
    conn.commit()
    conn.close()
    print("hola1")
    return "True"

@app.route("/newName", methods=["GET", "PUT"])
def update():
  if request.method == "PUT":
    id = request.form['id']
    print(id)
    nombreNuevo = request.form["newname"]
    print(nombreNuevo)
    conn = sqlite3.connect("truco.db")
    new = f"""UPDATE Usuarios SET usuario ='{nombreNuevo}' WHERE Id ={id}"""
    conn.execute(new)
    conn.commit()
    conn.close()

    return "true"
    
    

@app.route("/unirse/<int:id>")
def sala(id):
  session['id_partida'] = id
  conn = sqlite3.connect("truco.db")
  o = f"""SELECT roomname FROM Sala WHERE Id = {id}"""
  roomname = conn.execute(o).fetchone()[0]
  x = f"""SELECT Id FROM Sala WHERE Id = {id}"""
  d = conn.execute(x).fetchone()[0]
  z = f"""SELECT a30 FROM Sala WHERE Id = {id}"""
  puntos = conn.execute(z).fetchone()[0]
  return render_template("juego.html",nombre = roomname, id = d, puntos = puntos)

@app.route("/usuarios/", methods=["GET", "DELETE"])
def selectThem():
  admin = session['admin']
  conn = sqlite3.connect("truco.db")
  x = """SELECT * FROM Usuarios WHERE usuario NOT LIKE 'admin'"""
  usuarios = conn.execute(x).fetchall()
  conn.close()
  return render_template("usuarios.html", cantUsuarios = usuarios, admin = admin)

@app.route('/obtenerId')
def id():
  return jsonify(session['nombre'])

@socketio.on('juego')
def pantalla():
  emit('pantalla', to=session['id_partida'])
  
@socketio.on('unirse')
def unirse():
  db = sqlite3.connect('truco.db')
  db.execute(f"""UPDATE Usuarios
                  SET id_partida = {session['id_partida']}
                  WHERE usuario = '{session['nombre']}'""")
  db.commit()
  usuarios = db.execute(f"""SELECT usuario FROM Usuarios WHERE id_partida = {session['id_partida']}""")
  jugadores = []
  for i in usuarios:
    print(i)
    jugadores.append(i[0])
  db.close()

  data = {"jugadores":jugadores, "id":session['nombre'], "id_partida":session['id_partida']}
  print(session['id_partida'])
  room = session['id_partida']
  print(room)
  join_room(room)
  print("me uni")
  emit('jugadores', data, to=session['id_partida'])

@socketio.on('usuarios')
def usuarios():
  db = sqlite3.connect("truco.db")
  nombres = db.execute(f"""SELECT usuario FROM Usuarios WHERE Id = {session['id_partida']}""")
  if len(nombres) == 2:
    up = """UPDATE Sala SET Llena = 'Si'"""
    db.execute(up)
    
  
  print(nombres)
  nombreses = nombres.fetchall()
  jugadores = []
  for i in nombreses:
    print(nombreses[i])
    jugadores.append(nombreses[i])
  db.close()
  data = {"jugadores":jugadores, "id":session['nombre']}
  print(data)
  emit('jugadores', data)

@socketio.on('comenzar')
def comenzar(jugadores_js):
  session['ronda'] = 0
  conn = sqlite3.connect("truco.db")
  mazoJ = mazo
  random.shuffle(mazoJ) #Mezclo el mazo
  mazoJuego = [] #Creo el mazo que le voy a pasar al js
  x = """SELECT * FROM Cartas"""
  for i in range (40):
    y = conn.execute(x).fetchall()[i]
    carta = {
      "valor"  :  y[4],
      "numero" :  y[2],
      "palo"   :  y[3],
      "url"    :  y[5],
    }
    mazoJuego.append(carta)
  for i in jugadores_js['jugadores']:
    print(i)
    cartas = []
    for l in range(3): #Para que cada jugador tenga 3 cartas
      random.shuffle(mazoJuego)
      print(mazoJuego[l])
      cartas.append(mazoJuego[l]) #Agrego la primera carta del mazo 

    jugador = {"nombre":i, "cartas":cartas}
    if i == session['nombre']:
      player = i
      print(i, ", ", session['nombre'])
      print(jugador)
      emit("repartir", jugador, to=session['id_partida'])

  session['mazo'] = mazoJuego
  print(jugadores_js)
  print(player)
  truco = "truco"
  emit('trucar', truco)
  emit('jugar', player, to=session['id_partida'])

  
@socketio.on('nuevaRonda')
def nuevaRonda():
  data = session['ronda']
  session['ronda'] += 1
  print(data)
  emit('seguir', data, to=session['id_partida'])

@socketio.on('nuevaMano')
def nuevaMano():
  session['ronda'] = 0
  data = session['ronda']
  emit('seguir', data, to=session['id_partida'])

@socketio.on('recibirCartaDelOponente')
def recibirCartaDelOponente(data, pos):
  print("recibido")
  print(data)
  print(pos)
  datas = [data, pos]
  print(datas)
  emit('recibirCartaDelOponente', data, to=session['id_partida'])

@socketio.on('salir')
def salir():
  room = session['id_partida']
  leave_room(room)

@socketio.on('truco')
def truco(data):
  puntos = 1
  if data == "truco":
    puntos = 2
  elif data == "retruco":
    puntos = 3
  elif data == "valeCuatro":
    puntos = 4
  emit('trucar', data)
  emit('puntosEnJuego', puntos, to=session['id_partida'])
  
@socketio.on('envido')
def envido(data):
  # data es una mezcla entre la cantidad de puntos
  punto = data[0]
  if data[1] == 2:
    punto += 2
    emit('envidar', "envido")
  elif data[1] == 3:
    punto += 3
    emit('envidar', "realEnvido")
  elif data[1] == 4:
    punto +=2
    emit('envidar', "dobleEnvido")
  elif data[1] == 5:
    emit('envidar', "faltaEnvido")
    
  emit('puntosEnJuego', punto, to=session['id_partida'])


@app.route("/trucos", methods=["GET", "POST"])
def trucos():
  if request.method == "POST":
    truco = 0
    canta = request.form["truco"]
    respuesta = request.form["querer"]
    puntos = request.form["puntos"]
    if canta == "Truco":
      return "True"
      truco += 1
      if respuesta == "Quiero":
        puntos += 2
      elif canta == "Retruco":
        truco += 1
        if respuesta == "Quiero":
          puntos += 3
        elif canta == "Vale Cuatro":
          truco += 1
          if respuesta == "Quiero":
            puntos += 4
          else:
            puntos += 3
        else:
          puntos += 2
      else:
        puntos += 1
        pass

@app.route("/envido", methods=["GET", "POST"])
def envido():
  if request.method == "POST":
    envido = 0
    canto = request.form["envido"]  
    respuesta = request.form["querer"]
    puntos = request.form["puntos"]
    if canto == "Envido":
      envido += 1
      if respuesta == "Quiero":
        puntos += 2
      elif canto == "Envido":
        if respuesta == "Quiero":
          puntos += 4
        elif canto == "Real Envido":
          envido += 1
          if respuesta == "Quiero":
            puntos += 7
          elif canto == "Falta Envido":
            envido += 1
            if respuesta == "Quiero":
              puntos += 30
            else:
              puntos += 7
          else:
            puntos += 4
        elif canto == "Falta Envido":
          envido += 2
          if respuesta == "Quiero":
            puntos += 30#*
          else:
            puntos += 4
        else:
          puntos += 2
      elif canto == "Real Envido":
        envido += 1
        if respuesta == "Quiero":
          puntos += 5
        elif canto == "Falta Envido":
          envido += 1
          if respuesta == "Quiero":
            puntos += 30 #*
          else:
            puntos += 5
        else:
          puntos += 2
      elif canto == "Falta Envido":
        envido += 2
        if respuesta == "Quiero":
          puntos += 30
        else:
          puntos += 2
      else:
        puntos += 1
    elif canto == "Real Envido":
      envido += 2
      if respuesta == "Quiero":
        puntos += 3
      elif canto == "Falta Envido":
        envido += 1
        if respuesta == "Quiero":
          puntos += 30 #*
        else:
          puntos += 3
      else:
        puntos += 1
    elif canto == "Falta Envido":
      envido += 3
      if respuesta == "Quiero":
        puntos += 30 #*
      else:
        puntos += 1

@socketio.on('disconnect')
def desconectar():
  db = sqlite3.connect('truco.db')
  db.execute(f"""UPDATE Usuarios
                  SET id_partida = NULL
                  WHERE usuario = '{session['nombre']}'""")
  db.commit()
  
  db.close()
  
  
  
if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=81)

app.run(host='0.0.0.0', port=81)


            
  
  