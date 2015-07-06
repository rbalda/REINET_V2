$(document).ready(function() {
	
	$('.button').click(function() {
		
		type = $(this).attr('data-type');
		
		$('.overlay-container').fadeIn(function() {
			
			window.setTimeout(function(){
				$('.window-container.'+type).addClass('window-container-visible');
			}, 100);

		});
    centraVentana($('.overlay-container'));


	});
    $('.aceptar').click(function(){
        var id=$(this).attr('id');
        $('#eliminarEnviado').attr('href',"/eliminarMensajeEnviado/?q=".concat(id));
    });
    $('.aceptar').click(function(){
        var id=$(this).attr('id');
        $('#eliminarRecibido').attr('href',"/eliminarMensajeRecibido/?q=".concat(id));
    });
	
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