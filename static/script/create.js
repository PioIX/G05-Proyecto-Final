function crear(){
    let form = document.getElementById("form").elements;
    let nombre = form["nombre"].value;
    let puntos = form["puntos"].value;
    let contra = form["contra"].value;

    console.log(nombre, puntos)
    if(nombre == "" || puntos == ""){
        return alert('Faltan datos por rellenar')
    }else{
        $.ajax({
            url:"/crearMesa",
            type:"POST",
            data:{"nombre":nombre, "puntos":puntos, "contra":contra},
            success: function(response){
                if(response == 'True'){
                    alert('Mesa creada con exito')
                    location.href = "/salaDeEspera/"
                }else{
                    alert('Ha habido un error')
                }
            },
            error: function(error){
                console.log(error);
        }, });
    }
    
    
}