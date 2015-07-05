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