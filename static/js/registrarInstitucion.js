
function readURL(input) {
if (input.files && input.files[0]) {
	var reader = new FileReader();

	reader.onload = function (e) {
		$('#blah')
			.attr('src', e.target.result)
			.width(200)
			.height(200);
	};

	reader.readAsDataURL(input.files[0]);
}
}

$("#paisInstitucion").change(function () {
  $.ajax({
    type: "POST",
    url: "/getCiudades",
    data: {
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
        'paisId' : $("#paisInstitucion option:selected").val()
    },
    success: ciudadSuccess,
    dataType: 'html'
  });
});

function ciudadSuccess(data, textStatus, jqXHR){
$("#optsCiudades").html(data);
}


/*
Autor: Sixto Castro
Nombre de función: validarNumero
Parámetros: evento(e)
Salida:  Permite solo ingreso de números
Descripción: No permite el ingreso de letras

*/
//Función que permite solo Números
function validarNumero(e){

	var key = window.Event ? e.which : e.keyCode
    /*Edicion: Ray Montiel
      Descripcion: Se permite el caracter '+' para ingresar números por códigos de región, ejemplo: +593 123 456 789
    */
    return (key >= 48 && key <= 57 || key == 43 || key == 8)
}



 function validarLetras(e){
   key = e.keyCode || e.which;
   tecla = String.fromCharCode(key).toLowerCase();
   letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
   especiales = "8-37-39-46";

   tecla_especial = false
   for(var i in especiales){
		if(key == especiales[i]){
			tecla_especial = true;
			break;
		}
	}

	if(letras.indexOf(tecla)==-1 && !tecla_especial){
		return false;
	}
}


function validarURL (abc) {
	var string = abc.value;
	if (!~string.indexOf("http")){
		string = "http://" + string;
	}
	abc.value = string;
	return abc
}

/////////////////////////////////////////////////////////
/*
$("#siglaInstitucion").keyup(function () {
    console.log($("#siglaInstitucion").val());
    habilitarDeshabilitarSubmit(0);
    $.ajax({
        type: "POST",
        url: "/verificar_siglas",
        data: {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            'siglas': $("#siglaInstitucion").val()
        },
        success: verificaSiglas,
        dataType: 'text'
    });
});

$("#siglaInstitucion").change(function () {
    console.log($("#siglaInstitucion").val());
    habilitarDeshabilitarSubmit(0);
    $.ajax({
        type: "POST",
        url: "/verificar_siglas",
        data: {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            'siglas': $("#siglaInstitucion").val()
        },
        success: verificaSiglas,
        dataType: 'text'
    });
});

function habilitarDeshabilitarSubmit(valor) {

    if (valor == 0) {
        $("#continuar").removeAttr("enabled");

        $("#continuar").attr("disabled", "disabled");
    }else{
        $("#continuar").removeAttr("disabled");

        $("#continuar").attr("enabled", "enabled");
    }
}

function verificaSiglas(data, textStatus, jqXHR) {
    console.log(data);
    if (data == "usado") {
        $("#sigla_usada").html("Siglas para su instituci&oacute;n no v&aacute;lidas. Debe tener m&iacute;nimo 3 caracters y debe ser unica");
        $("#sigla_usada").attr("style", "display: block; color: red; text-align:center");
        $("#sigla_usada").attr("class", "info-board-red");
        habilitarDeshabilitarSubmit(0);
    }
    else {
        $("#sigla_usada").html("Siglas disponibles para su instituci&oacute;n");
        $("#sigla_usada").attr("style", "display: block; color: green; text-align:center");
        $("#sigla_usada").attr("class", "info-board-green");
        habilitarDeshabilitarSubmit(1);
    }
}*/