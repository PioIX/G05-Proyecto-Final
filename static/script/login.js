function login(){
    let form = document.getElementById("login").elements;
    let nombre = form["nombre"].value;
    let contra = form["contra"].value;

    console.log(nombre, contra)
    if(nombre == "" || contra == ""){
        return alert('Faltan datos por rellenar')
    }else{
        $.ajax({
            url:"/log",
            type:"POST",
            data: {nombre:nombre, contra:contra},
            success: function(response){
                if(response == 'True'){
                  location.href = "https://Memotest.nicolasgr8.repl.co/inicio";
                  alert('Inicio de sesion exitosa')
                }else{
                    alert('No existe ese usuario')
                }
            },
            error: function(error){
                console.log(error);
        }, });
    }
    
    
}