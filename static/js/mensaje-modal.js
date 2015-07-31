/*
Autor: Leonel Ramirez
Nombre de la funcion: scrip para el modal mensaje  
Parámetros: eventos
Salida: Al activarse el evento aparece automaticamente un modal con un mensaje de confirmacion
Descripción: la funcion que se encuentran a continuacion  muestra el mensaje de confirmacion de forma de un modal
"""
*/
$(document).ready(function() {
	
	$('.button').click(function() {
		
		type = $(this).attr('data-type');
		
		$('.overlay-container').fadeIn(function() {
			
			window.setTimeout(function(){
				$('.window-container.'+type).addClass('window-container-visible');
			}, 100);

		});
    centraVentana($('.overlay-container'));

/*
Autor: Marlon Espinoza
Nombre del archivo: script que obtiene el id
Parámetros: eventos
Salida: obtiene el id del mensaje a eliminar
Descripción: al dar clinck en el evento obtiene el id del mensaje que es elije para ser eliminado hay
             4 funciones a continuacion tienen el mismo funcionamiento pero para cada tipo de mensaje
             como eliminarMensajeEnviadoInstitucion
*/

	});
    $('.aceptar').click(function(){
        var id=$(this).attr('id');
        $('#eliminarEnviado').attr('href',"/eliminarMensajeEnviado/?q=".concat(id));
    });
    $('.aceptar').click(function(){
        var id=$(this).attr('id');
        $('#eliminarRecibido').attr('href',"/eliminarMensajeRecibido/?q=".concat(id));
    });

    //esto es para las mensajeria de instituciones
    $('.aceptar_institucion').click(function(){
        var id=$(this).attr('id');
        $('#eliminarEnviadoInstitucion').attr('href',"/eliminarMensajeEnviadoInstitucion/?q=".concat(id));
    });
    $('.aceptar_institucion').click(function(){
        var id=$(this).attr('id');
        $('#eliminarRecibidoInstitucion').attr('href',"/eliminarMensajeRecibidoInstitucion/?q=".concat(id));
    });


/*
Autor: Leonel Ramirez
Nombre de la funcion: scrip para cerrar el modal 
Parámetros: eventos
Salida: cierra le modal 
Descripción: al dar clic en el boton cerra o cancelar se cierra automaticamente el modal
*/

	$('.close').click(function() {
		$('.overlay-container').fadeOut().end().find('.window-container').removeClass('window-container-visible');
	});
    $("button[name='close']").click(function() {
		$('.overlay-container').fadeOut().end().find('.window-container').removeClass('window-container-visible');
	});
	$('.enviar').click(function(){
       if($('.destinatario').text()){

       }
    });


/*
Autor: Marlon Espinoza
Nombre de la funcion: scrip para centrar el modal en la ventana 
Parámetros: eventos
Salida: centra el modal del mensaje de confirmacion
Descripción: la funcion se encarga de centrar el modal
*/

    function centraVentana(ventana){

        //dimensiones de la ventana del cliente

        var anchoCliente = document.documentElement.clientWidth;

        var altoCliente = document.documentElement.clientHeight;

        ventana.css("position","absolute");
        //dimensiones de la ventana que nos llega

        var anchoVentana = ventana.width();

        var altoVentana = ventana.height();

        //centramos la ventana con los cálculos necesarios

        ventana.css("left",(anchoCliente-2*anchoVentana)/2);

        ventana.css("top",Math.max(10,(altoCliente-2*altoVentana)/2)+$(window).scrollTop());

    }

});