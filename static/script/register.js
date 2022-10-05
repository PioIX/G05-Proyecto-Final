function registrarse(){
  let form = document.getElementById("login").elements;
    let nombre = form["nombre"].value;
    let contra = form["contra"].value;

    console.log(nombre, contra)
    if(nombre == "" || contra == ""){
        return alert('Faltan datos por rellenar')
  }else{
    console.log(nombre, contra)
    $.ajax({
        url:"/register",
        type:"POST",
        data: {nombre:nombre, contra:contra},
        success: function(respuesta){
          if(respuesta == 'True' ){
            alert(nombre + ' añadido a la base de datos')
          }else{
            alert(respuesta)
          }
        },
        error: function(error){
            console.log(error);
        }, 
    });
  }  
};

