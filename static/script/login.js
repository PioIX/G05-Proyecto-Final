function login(){
    let form = document.getElementById("login").elements;
    let nombre = form["nombre"].value;
    let contra = form["contra"].value;

    console.log(nombre, contra)
    if(nombre == "" || contra == ""){
        return alert('Faltan datos por rellenar')
    }else{
        $.ajax({
            url:"/iniciado",
            type:"POST",
            data: {nombre:nombre, contra:contra},
            success: function(response){
                if(response == 'False'){
                  alert('No existe ese usuario')
                }else{
                  alert('Inicio de sesion exitosa')
                  location.href = '/salaDeEspera/'
                }
            },
            error: function(error){
                console.log(error);
        }, });
    }
    
    
}