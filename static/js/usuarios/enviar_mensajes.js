$('#destinatario').on('keyup change', function (evt) {
    var destinatario = $('#destinatario').val();
    var username = "{{usuario.username}}";
    console.log(destinatario.toLowerCase());
    console.log('emisor' + username);
    if (destinatario.toLowerCase() == username.toLowerCase()) {
        document.getElementById("divAlertaUsuario").style.display = 'block';
        $('.mensaje_error').text("No puedes enviarte el mensaje a ti mismo");
        $('#btn_enviar_mensaje_nuevo').attr('disabled', true);
    } else if (destinatario != usuario) {
        document.getElementById("divAlertaUsuario").style.display = 'none';
        $('#btn_enviar_mensaje_nuevo').attr('disabled', false);
    }
});