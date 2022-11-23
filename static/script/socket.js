let socket = io();
socket.emit('unirse')
// socket.emit('usuarios')
let id_partida
let id
let j
let jugadores
let cartas_jugador
let cartas_jugadas = []
let cartas = []
let cartasEnemigo = 3


socket.on('jugadores', (data)=>{
  jugadores = data['jugadores'] 
  console.log(jugadores)
  console.log("2")
  console.log(id)
  id_partida = data["id_partida"]
  // Preparo esperando para introducir a los jugadores
  document.getElementById('esperando').innerHTML = ""
  for(let i = 0; i < jugadores.length; i++){
    //Imprimo cada jugador en pantalla de espera
    document.getElementById('esperando').innerHTML += `<strong><p class="esperando">Jugadores: ${jugadores[i]}</p></strong>`
  }
  boton_jugar = document.getElementById("boton_jugar")
  if(jugadores.length > 1){
    //Cuando hay mas de un jugador se habilita el boton para comenzar el juego
    boton_jugar.classList.remove('inactivo')
    boton_jugar.addEventListener("click", ingame)
  }else {
    boton_jugar.classList.add('inactivo')
    //Cuando hay menos de un jugador se deshabilita el boton para comenzar el juego
    boton_jugar.removeEventListener("click", ingame)
  }
})

function turnos(){
  console.log("turnos")
  console.log(cartas_jugador)
  console.log(id)
  console.log(jugadores)
  if (id == jugadores[0]){
    console.log(id)
    console.log(cartas_jugador)
    console.log(cartas)
  for(let i = 1; i < 4; i++){
    console.log(i)
    cartas_jugador = document.getElementById("carta" + `${i}`)
    console.log(cartas_jugador)
    console.log(cartas[i-1])
    cartas_jugador.addEventListener("click", ()=>{tirar(i-1, cartas[i-1])}, true)

    
                                    //= function (){
      //console.log(data_jugador.cartas[i])
      //remove = jugar(data_jugador.cartas[i])
      //console.log(remove)
      //if(remove){
        //this.remove()
        //cartas_jugador.splice(i, 1)
        //data_jugador.cartas.splice(i, 1)
        
        //for(let l = 0; l < cartas_jugador.length; l++){
          //cartas_jugador[i].removeEventListener("click", tirar)  
          //cartas_jugador[l].outerHTML = cartas_jugador[l].outerHTML
        //}
        //console.log("Turno: ", turno)
        //data = {carta: cartaJugadaFlask, turno:turno, id:id}
        //socket.emit('jugada', data)
      //}
    //})
}}
}

function jugar(carta){
  console.log(carta)
  cartaJugadaFlask = carta
  return true
}

$.ajax({
  
  url:"/obtenerId",
  
  type:"GET",
  
  data: {"value":0},
  
  success: function(response){
    id = response
  },
  error: function(error){
  //console.log(error);
  
  }, });

socket.on('jugar', (data)=>{
  console.log("3")
  console.log(id)
  console.log(data)
  if(id==data && cartas_jugador != null){
    levantada = false
    turnos()
    }
})

socket.on('seguir', (data)=>{
  if(cartas_jugador != null){
    console.log(cartas)
    
    if (cartas.length < 3 && cartasEnemigo < 3){
      console.log("siguiendo", cartas.length)
      rondaDos()
    }
    cartasEnemigo -= 1
    levantada = false
    turnos()
    }
})


socket.on('trucar', (data)=> {
  // la data seria que truco/returco/o vale cuatro se pone visible, ya que solo puede haber uno, y si data esta vacio entonces no aparece nada, osea que ya se canto vale cuatro
  document.getElementById("truco").style.display = "none"
  document.getElementById("retruco").style.display = "none"
  document.getElementById("valeCuatro").style.display = "none"
  if (data != ""){
    document.getElementById(`${data}`).style.display = "block"
  }
})
socket.on('envidar', (data)=> {
  if (data == "envido"){
    console.log("envido")
  }
  if (data == "dobleEnvido"){
    document.getElementById("envido").style.display = "none"
  }
  if (data == "realEnvido"){
    document.getElementById("realEnvido").style.display = "none"
  }
  if (data == "faltaEnvido"){
    document.getElementbyId("faltaEnvido").style.display = "none"
  }
})

function envido(data){
  let data1 = [data]
  socket.emit('envido', data1)
}


socket.on('querer', (data)=> {
  // la data seria que boton especial puede usar, y que onclick hace el no quiero, osea cuantos puntos sumaria decir que no
  document.getElementById("truco").style.display = "none"
  document.getElementById("retruco").style.display = "none"
  document.getElementById("valeCuatro").style.display = "none"
  document.getElementById("quiero").style.display = "block"
  document.getElementById("noQuiero").style.display = "block"
  document.getElementById("noQuiero").innerHTML = `<button class="boton" type="submit" onclick='${data[1]}'><strong> 'No Quiero' </strong> </button>`
  if (data[0] != "envido"){
  document.getElementById("especial").innerHTML = `<button class="boton" type="submit" onclick='${data[0]}'><strong> '${data[0]}' </strong> </button>`
  }
})

socket.on('pasarTurno', (data)=> {
  let trucos = document.getElementsByName("truco")
  for (let i = 0; i < trucos.length; i++){
    trucos[i].disabled = true
  }
  let envidos = document.getElementsByName("envido")
  for (let i = 0; i < envidos.length; i++){
    envidos[i].disabled = true
  }
  document.getElementById("especial").innerHTML = ''
})

socket.on('volverTurno', (data)=> {
  let trucos = document.getElementsByName("truco")
  for (let i = 0; i < trucos.length; i++){
    trucos[i].disabled = false
  }
  let envidos = document.getElementsByName("envido")
  for (let i = 0; i < envidos.length; i++){
    envidos[i].disabled = false
  }
  document.getElementById("especial").innerHTML = ''
})

function rondaDos(){
  document.getElementById("envido").style.display = "none"
  document.getElementById("realEnvido").style.display = "none"
  document.getElementById("faltaEnvido").style.display = "none"
}

socket.on('tirarCarta', (data)=> {
  // la data seria la carta,  la posicion de la carta (tanto de la mano como en que parte de la mesa va a ser tirada)
  document.getElementById(`${data[1]}`).innerHTML = ''
  document.getElementById(`${data[2]}`).innerHTML = `<div class="cartas" style="background-image:url('${data[0].url}')"></div>`
})

socket.on('recibirCartaDelOponente', (data)=> {
  // aca solo se necesita que la data sea que carta es y la posicion en la mesa
  console.log(data)
  if(id == jugadores[1]){
  document.getElementById(`${data[1]}`).innerHTML = `<div class="cartas" style="background-image:url('${data[0]['url']}')"></div>`}
  jugadores = [jugadores[1], jugadores[0]]
  console.log(jugadores)
})

socket.on('jugadores', (data)=>{
  j = data
})

function ingame(){
  socket.emit('juego')
}


socket.on('pantalla', ()=> {
  console.log("Ejecute pantalla")
  document.getElementById("unirseMesa").style.display = "none"
  document.getElementById("juego").style.display = "block"
  // document.getElementById("nos").innerHTML = `<p> ${jugadores[0]}</p>`
  // socket.emit('comenzar', j)
  socket.emit('comenzar', j)
})



socket.on('repartir', (data)=> {
  jugadoreses = data
  console.log(jugadores)
  console.log("1")
  console.log(id)
  /*if (jugadoreses["nombre"] != id){
    cartasEnemigo = data['cartas']}*/
  if (jugadoreses["nombre"] == id){
    cartas = data['cartas']
  for(let l = 1; l < 4; l++){
    cartas_jugador = document.getElementById("carta" + `${l}`)
    cartas_jugador.innerHTML += `<div class="cartas" style="background-image:url('${jugadoreses['cartas'][l-1]['url']}')"></div>`
      } 
    }}
)

socket.on('carta', (data)=> {
  console.log(data)
})

socket.on('mensaje', (data)=>{
  console.log(data)
})

/*Funcion de las cartas para 'tirarlas'*/
function tirar(posicion, carta){
  console.log("Hola, me tiraste")
  i_eliminar = cartas[posicion] //Saco el index del elemento en su array para eliminarlo con ell splice
  console.log("i_eliminar:")
  console.log(i_eliminar)
  console.log(cartas)
  cartas.splice(i_eliminar, 1)
  console.log(cartas)
  carta_jugada = carta //La carta jugada pasa a ser la que acabo de tirar
  let posicionDeLaMesa
  let posiiconDeLaMesaContraria
  for (let i = 3; i > 0; i--){
    pos = document.getElementById("cartaTuya" + `${i}`)
    posContraria = "cartaSuya" + `${i}`
    console.log(pos)
    console.log(pos.innerHTML)
    if (pos.innerHTML == ''){
      posicionDeLaMesa = pos
      posicionDeLaMesaContraria = posContraria
      console.log("mesa contraria", posicionDeLaMesaContraria)
    }
  }
  posicionHTML = posicion + 1
  console.log(posicionDeLaMesa)
  cartaHTML = document.getElementById("carta" + `${posicionHTML}`)
  posicionDeLaMesa.innerHTML = cartaHTML.innerHTML
  cartaHTML.innerHTML = ''
  for (let i = 1; i < 4; i++){
    console.log("hola")
    posic = document.getElementById("carta" + `${i}`)
    posic.outerHTML = posic.outerHTML
  }
  
  let datazo = [carta, posicionDeLaMesaContraria]
  console.log(datazo)
  console.log(id_partida)
  socket.emit('recibirCartaDelOponente', datazo, posicionDeLaMesaContraria)
  socket.emit('nuevaRonda')
  // calcular_turno(objeto.tipo)
  //socket.emit('tire', id)
  //if(cartas.length == 1){
  //  document.getElementById('partida').innerHTML += '<img id="boton_uno" class="boton_uno tirable" src="../../static/media/images/uno.png" alt="UNO">'
  //}else if(cartas.length == 0){
  //  socket.emit('ganar', id)
  //}
}

function envido(){
  envido = document.getElementById("envido").value
    $.ajax({
      url:"/envido",
      type:"POST",
      data: {"envido": envido},
      success: function(response){
        if (response == "True"){
          alert("Funciona")
        }else{
          alert("No funciona")
        }
      },
      error: function(error){
        console.log(error)}
        
    })
      
      
    
}

