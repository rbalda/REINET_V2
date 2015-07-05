$(document).ready(function() {
	
	$('.button').click(function() {
		
		type = $(this).attr('data-type');
		
		$('.overlay-container').fadeIn(function() {
			
			window.setTimeout(function(){
				$('.window-container.'+type).addClass('window-container-visible');
			}, 100);

		});
        $('.overlay-container').position({
                my: "center",
                at: "center",
                of: window
            });


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
});