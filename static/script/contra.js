function contra(id){
    let form = document.getElementById(id).elements;
    let contra = form["contra"].value;

    console.log(contra)
    if(contra == ""){
        return alert('Falta la contraseña')
    }else{
        $.ajax({
            url:"/iniciado2",
            type:"POST",
            data: {contra:contra, id:id},
            success: function(response){
                if(response == 'False'){
                  alert('Contraseña Incorrecta')
                }else{
                  location.href = '/unirse/'+id
                }
            },
            error: function(error){
                console.log(error);
        }, });
    }
    
    
}