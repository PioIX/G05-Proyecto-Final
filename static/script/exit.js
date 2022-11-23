function eliminar(){
    let id = document.getElementById('id').innerHTML
    console.log(id)
    $.ajax({
    url:"/eliminarMesa",
    type:"DELETE",
    data: {id:id},
    success: function(response){
        if(response == 'True'){
            location.href="/salaDeEspera/"
        }else{
            alert('Ha ocurrido un error.')
        }
    },
    error: function(error){
        console.log(error);
}, });
}

function eliminarV2(id){
    console.log(id)
    $.ajax({
    url:"/eliminarMesa",
    type:"DELETE",
    data: {id:id},
    success: function(response){
        if(response == 'True'){
            location.href="/salaDeEspera/"
        }else{
            alert('Ha ocurrido un error.')
        }
    },
    error: function(error){
        console.log(error);
}, });
}

function eliminar2(id){
    console.log(id)
    $.ajax({
    url:"/eliminarUsuario",
    type:"DELETE",
    data: {id:id},
    success: function(response){
        if(response == 'True'){
            location.href="/usuarios"
        }else{
            alert('Ha ocurrido un error.')
        }
    },
    error: function(error){
        console.log(error);
}, });
}

function actualizar(id){
    console.log(id)
    $.ajax({
      url: "/newName",
      type: "PUT",
      data: {"id":id, 
            "newname":document.getElementById("newname").value},
      success: function(response){
          console.log(response)
          if(response == 'true'){
              location.href ="/usuarios"
              alert("Anduvo la cosa")
          }else{
              alert("Ta todo mal flaco")
          }
      },
      error: function(error){
          console.log(error);
    },
  });
}