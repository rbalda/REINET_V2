function inicializar(){
    var btnContinuar = document.getElementById("instBtnContinuar");
    btnContinuar.addEventListener("click",cargarFormulario,false);
}

function cargarFormulario(){
    var formulario = document.getElementById("instMainForm");

    if(formulario.hasChildNodes()){
        while(formulario.hasChildNodes()){
            formulario.removeChild(formulario.childNodes[0]);
        }
    }
    var contenedor = document.createElement("div");
    contenedor.setAttribute("class","form-group");


    var espacio = document.createElement("br");
    var espacio2 = document.createElement("br");
    var espacio3 = document.createElement("br");
    var espacio4 = document.createElement("br");
    var espacio5 = document.createElement("br");
    var espacio6 = document.createElement("br");
    var espacio7 = document.createElement("br");


    //nombreInstitucion
    var nombre = document.createElement("input");
    nombre.setAttribute("class","form-control");
    nombre.setAttribute("id","nombreInstitucion");
    nombre.setAttribute("placeholder","Nombre de la Institución");

    //siglaInstitucion
    var sigla = document.createElement("input");
    sigla.setAttribute("class","form-control");
    sigla.setAttribute("id","siglaInstitucion");
    sigla.setAttribute("placeholder","Siglas/Nombre abreviado");

    //descripcionInstitucion
    var descripcion = document.createElement("input");
    descripcion.setAttribute("class","form-control");
    descripcion.setAttribute("id","descripcionInstitucion");
    descripcion.setAttribute("placeholder","Descripción");

    //misionInstitucion
    var mision = document.createElement("input");
    mision.setAttribute("class","form-control");
    mision.setAttribute("id","misionInstitucion");
    mision.setAttribute("placeholder","Misión");

    //ubicacionInstitucion
    var ubicacion = document.createElement("input");
    ubicacion.setAttribute("class","form-control");
    ubicacion.setAttribute("id","ubicacionInstitucion");
    ubicacion.setAttribute("placeholder","Ubicación");

    //recursosInstitucion
    var recursos = document.createElement("input");
    recursos.setAttribute("class","form-control");
    recursos.setAttribute("id","recursosInstitucion");
    recursos.setAttribute("placeholder","Recursos Ofrecidos");

    //webInstitucion
    var web = document.createElement("input");
    web.setAttribute("class","form-control");
    web.setAttribute("id","webInstitucion");
    web.setAttribute("placeholder","Dirección web");


    //Boton Crear y terminos y condiciones
    var check = document.createElement("div");
    check.setAttribute("class","checkbox");
    var chkTxt = document.createTextNode("Estoy de acuerdo con los Términos de servicio y las Políticas de Privacidad");
    var lab = document.createElement("label");
    var inp = document.createElement("input");
    inp.setAttribute("type","checkbox");
    lab.appendChild(chkTxt);
    lab.appendChild(inp);
    check.appendChild(lab);
/**
     Estoy de acuerdo con los <a href="#">Términos de servicio</a> y las
                  <a href="#">Politicas de Privacidad</a>
     <button id="instBtnContinuar" type="submit" class="btn btn-green">Continuar</button>
*/
    var btnCrear = document.createElement("button");
    var btnTxt = document.createTextNode("Crear Cuenta");
    btnCrear.setAttribute("id","instBtnCrear");
    btnCrear.setAttribute("type","submit");
    btnCrear.setAttribute("class","btn btn-green");
    btnCrear.appendChild(btnTxt);


    contenedor.appendChild(nombre);
    contenedor.appendChild(espacio);
    contenedor.appendChild(sigla);
    contenedor.appendChild(espacio2);
    contenedor.appendChild(descripcion);
    contenedor.appendChild(espacio3);
    contenedor.appendChild(mision);
    contenedor.appendChild(espacio4);
    contenedor.appendChild(ubicacion);
    contenedor.appendChild(espacio5);
    contenedor.appendChild(recursos);
    contenedor.appendChild(espacio6);
    contenedor.appendChild(web);
    contenedor.appendChild(espacio7);
    contenedor.appendChild(check);
    contenedor.appendChild(btnCrear);
    formulario.appendChild(contenedor)
}



window.addEventListener("load", inicializar, false);