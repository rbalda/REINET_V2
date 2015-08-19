/*
 * Autor: Fausto Mora
 Nombre de función: script para validar las passwords
 Salida: Muestra advertencia si son distintos, no cumplen el tamaño y 
 bloquean la accion de ingreso
 Descripción: Compara que password 1 y 2 sean iguales, que cumpla el tamano
 entre 4 a 15 caracteres
 Nota: las funciones se implementan con nombres de clases para poder generalizar 
 el script y que se pueda usar para otras validaciones similares
 * */

$(document).ready(function () {
	console.log('dentro de verificar-password')

	$.getScript("/static/js/jquery.cookie.js", function(){

		});

	activarBoton();

	var error_iguales = 'Las contraseñas no coinciden';
	var error_tam = 'La contraseña debe contener entre 4 a 15 caracteres';
	var valido_iguales = false;
	var valido_tam = false;

	$('.passwordSet2').keyup(function(evt){
		var pass1 = $('.passwordSet1').val();
		var pass2 = $('.passwordSet2').val();

		if(pass1!=pass2){
			$('.mensaje_error').text(error_iguales);
			$('.mensaje_error').addClass('alert alert-danger');
			$('.mensaje_error').fadeIn();
			valido_iguales = false;
		}else if(pass1=pass2){
			$('.mensaje_error').fadeOut();
			valido_iguales = true;
		}

		activarBoton();
		
	});

	$('.passwordSet1').keyup(function(evt){
		var pass1 = $('.passwordSet1').val();

		if(pass1.length > 3 && pass1.length <16){
			$('.mensaje_error').fadeOut();
			$('.passwordSet2').attr('disabled',false);
			valido_tam = true;
		}else{
			$('.mensaje_error').text(error_tam)
			$('.mensaje_error').addClass('alert alert-danger');
			$('.mensaje_error').fadeIn();
			$('.passwordSet2').attr('disabled',true);
			valido_tam = false;
		}
	});

	function activarBoton(){
		if(valido_tam && valido_iguales){
			$('.btn_confirmar_password').attr('disabled', false);
		}else{
			$('.btn_confirmar_password').attr('disabled', true);
		}
	}


// parte especifica para cambiar contraseña por el usuario

	$("#passwordActual").change(function () {
        console.log($("#passwordActual").val());
        $.ajax({
            type: "POST",
            url: "/verificar_contrasena/",
            data: {
                'passwordActual': $("#passwordActual").val(),
                'csrfmiddlewaretoken' : $.cookie('csrftoken')
            },
            success: function(data){
                var objeto = JSON.parse(data);
                console.log(objeto);
                if (objeto.estado_password){
                	$('#error_password_incorrecta').fadeOut();
                	$('.passwordSet1').attr('disabled',false);
                }else{
                	$('#error_password_incorrecta').addClass('alert alert-danger');
                	$('#error_password_incorrecta').fadeIn();
                	$('#error_password_incorrecta').text('Contraseña incorrecta');
                	$('.passwordSet1').attr('disabled',true);
                }
            }
        });
    });

// parte especifica de suspender cuenta por el usuario

/*
 Autor: Kevin Zambrano y Fausto Mora
 Nombre de funcion: funciones anonimas
 Entrada: eventos
 Salida: http
 Descripción: genera un handler para los eventos en la interaccion con suspender cuenta usuario
 */

    $('#btn_suspenderCuenta').attr('disabled', 'disabled');
    $('#txt_password_ingresada').keyup(function () {
        $('#btn_suspenderCuenta').removeAttr('disabled');
    });
    $('#btn_suspenderCuenta').popover({
        html: true,
        content: function () {
            return $('#popover_content_wrapper').html();
        }
    });


// fin del script
});