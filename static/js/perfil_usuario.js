
function fijarReputacion() {
    try{
    var a = document.getElementsByClassName("rating")[0];
    var reputacion = parseInt(document.getElementById("reputacion-calificacion").innerHTML);
    if (reputacion <= 0) {
                                                    //a.style.display = "none";
    }
    else {
        var estrellitas = a.children;
        var i = 0;
        for (i = 0; i < reputacion; i++) {
            estrellitas[i].innerHTML = "\u2605";
        }

    }
    convertirFecha();
        }catch(e){

        }
}
function convertirFecha(){
    var td_fecha=document.getElementsByClassName("fecha_registro")[0];
    var fecha=String((document.getElementsByClassName("fecha_registro")[0]).innerHTML);
    var f=fecha.split(' ',3);

    var mes = f[0];
    var dia = f[1].split(',',1);
    var año= f[2].split(',',1);
    switch (mes) {
            case "January":
                mes = "Enero";
            break;
            case "February":
                mes = "Febrero";
                break;
            case "March":
                mes = "Marzo";
                break;
            case "April":
                mes = "Abril";
                break;
            case "May":
                mes = "Mayo";
                break;
            case "June":
                mes = "Junio";
                break;
            case "July":
                mes = "Julio";
                break;
            case "August":
                mes = "Agosto";
                break;
            case "September":
                mes = "Septiembre";
                break;
            case "October":
                mes = "Octubre";
                break;
            case "November":
                mes = "Noviembre";
                break;
            case "December":
                mes = "Diciembre";
                break;
    }
                                                
    td_fecha.innerHTML=dia+'/'+mes+'/'+año;

}                                           
window.onload = fijarReputacion;                                            
                                                