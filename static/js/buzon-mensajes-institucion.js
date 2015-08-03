var tipo = "emisor";

sessionStorage.setItem('pagina',1);

$('#info_mensaje_enviado').hide();

function bloquearBotones(){
    $('#buzon_entrada_institucion').attr('disabled',true);
    $('#buzon_salida_institucion').attr('disabled',true);
    $('#nuevo_mensaje_institucion').attr('disabled',true);
    $('#panel_mensajes').attr('disabled',true);
}

function desbloquearBotones(){
    $('#buzon_entrada_institucion').attr('disabled',false);
    $('#buzon_salida_institucion').attr('disabled',false);
    $('#nuevo_mensaje_institucion').attr('disabled',false);
    $('#panel_mensajes').attr('disabled',true);
}

function limpiarInputsMensajes(){
    $('#destinatario').val("");
    $('#asunto').val("");
    $('#mensaje').val("");
}

function camposVacios(){
    if ( ($('#destinatario').val()=="") || ($('#asunto').val()=="") ){
        $('#btn_enviar_mensaje_nuevo').attr('disabled',true);
    }else{
        $('#btn_enviar_mensaje_nuevo').attr('disabled',false);
    }
}

function buzonEntradaInstitucion() {
    console.log('dentro de buzon de entrada institucion');
    $.ajax({
        type: 'get',
        url: '/BandejaDeEntradaInstitucion/',
        data: {
            'pagina': sessionStorage.getItem('pagina'),
            'usuario_id': usuario
        },
        beforeSend: function(){
            bloquearBotones();
        },
        success: function (data) {
            $('#panel_mensajes').html(data);

        },
        complete: function(){
            desbloquearBotones();
        }
    });

}

function buzonSalidaInstitucion() {
    console.log('dentro de buzon salida institucion');
    $.ajax({
        type: 'get',
        url: '/BandejaDeSalidaInstitucion/',
        data: {
            'pagina': sessionStorage.getItem('pagina'),
            'usuario_id': usuario
        },
        beforeSend: function(){
            bloquearBotones();
        },
        success: function (data) {
            $('#panel_mensajes').html(data);
        },
        complete: function(){
            desbloquearBotones();
        }
    });

}

function nuevoMensajeInstitucion(){
    console.log('dentro de nuevo mensaje institucion');

    $.ajax({
        type:'get',
        url: '/nuevoMensajeInstitucion/',
        beforeSend: function(){
            bloquearBotones();
        },
        success: function (data) {
            $('#panel_mensajes').html(data);
        },
        complete: function(){
            camposVacios();
            desbloquearBotones();
        }
    });
}

function verMensajeInstitucion(id_mensaje){
    console.log('dentro de ver mensaje institucion');
    console.log('idmensaje ' + id_mensaje);

    $.ajax({
        type:'get',
        url: '/verMensajeInstitucion/',
        data:{
            'tipo_envio':tipo,
            'id_mensaje':id_mensaje
        },
        beforeSend: function(){
            bloquearBotones();
        },
        success: function (data) {
            $('#panel_mensajes').html(data);
        },
        complete: function(){
            desbloquearBotones();
        }
    });
}

function eliminarMensajeInstitucion(id_mensaje){
    console.log('dentro de eliminar mensaje institucion');
    console.log('idmensaje' + id_mensaje);

    $.ajax({
        type:'post',
        url: '/eliminarMensajeInstitucion/',
        data:{
            'tipo_envio':tipo,
            'id_mensaje':id_mensaje,
            'csrfmiddlewaretoken' : $.cookie('csrftoken')
        },
        success: function (data) {
            var objeto = JSON.parse(data);
            if(objeto.save_estado){
                mensaje_id = objeto.id_mensaje;
                $('#mensaje'+mensaje_id).remove();
            }else{
                alert('Error al eliminar mensaje');
            }
        }
    });

}

$(document).ready(function(){

       	$.getScript("/static/js/jquery.cookie.js", function(){

		});

        buzonEntradaInstitucion();

        $('#buzon_entrada_institucion').click( function () {
            tipo = "emisor";
            sessionStorage.setItem('pagina',1);
            buzonEntradaInstitucion();
        });

        $('#buzon_salida_institucion').click( function () {
            tipo = "receptor";
            sessionStorage.setItem('pagina',1);
            buzonSalidaInstitucion();
        });


       $('#nuevo_mensaje_institucion').click(function(){
           nuevoMensajeInstitucion();
       });

});

        $(document).on('click','.mensaje_mensaje',function(evt){
            console.log('click en un mensaje');
            id_mensaje=this.id;
            console.log(id_mensaje);
            console.log(tipo);

            if(id_mensaje!=null){
                verMensajeInstitucion(id_mensaje);
            }
        });

        $(document).on('click','.eliminar_mensaje',function(evt){
            console.log('click en eliminar mensaje');
            id_mensaje=this.id;
            console.log(id_mensaje);
            console.log(tipo);

            if(id_mensaje!=null){
                eliminarMensajeInstitucion(id_mensaje);
            }
        });



        $(document).on('click','.cancelar',function(){
              limpiarInputsMensajes();
        });

        $(document).on('click','#btn_siguiente_buzon_salida', function () {
            console.log('dentro del btn siguiente buzon salida');
            aux = parseInt(sessionStorage.getItem('pagina')) + 1;
            console.log(aux);
            sessionStorage.setItem('pagina',aux);
            buzonSalidaInstitucion();
        });

        $(document).on('click','#btn_anterior_buzon_salida', function () {
            console.log('dentro del btn anterior buzon salida');
            aux = parseInt(sessionStorage.getItem('pagina')) - 1;
            console.log(aux);
            sessionStorage.setItem('pagina',aux);
            buzonSalidaInstitucion();
        });

        $(document).on('click','#btn_siguiente_buzon_entrada', function () {
            console.log('dentro del btn siguiente buzon entrada');
            aux = parseInt(sessionStorage.getItem('pagina')) + 1;
            console.log(aux);
            sessionStorage.setItem('pagina',aux);
            buzonEntradaInstitucion();
        });

        $(document).on('click','#btn_anterior_buzon_entrada', function () {
            console.log('dentro del btn anterior buzon entrada');
            aux = parseInt(sessionStorage.getItem('pagina')) - 1;
            console.log(aux);
            sessionStorage.setItem('pagina',aux);
            buzonEntradaInstitucion();
        });


        $(document).bind('keyup change','#destinatario',function(evt){
            var destinatario = $('#destinatario').val();
            console.log(destinatario.toLowerCase());
            console.log('emisor' + username.toLowerCase());

            if(($('#destinatario').val()!="") && ($('#asunto').val()!="")){
                if(destinatario.toLowerCase()==username.toLowerCase()){
                    $('.mensaje_error').text("No puedes enviarte el mensaje a ti mismo");
                    $('.mensaje_error').addClass('alert alert-warning');
                    $('.mensaje_error').fadeIn();
                    $('#btn_enviar_mensaje_nuevo').attr('disabled',true);
                }else if(destinatario!= usuario) {
                    $('.mensaje_error').fadeOut();
                    $('.mensaje_error').text("");
                    $('.mensaje_error').removeClass('alert alert-warning');
                    $('#btn_enviar_mensaje_nuevo').attr('disabled', false);
                }
            }
	    });

        $(document).on('click','#btn_enviar_mensaje_nuevo', function () {
            console.log('dentro de enviar mensaje nuevo');
            console.log($('#destinatario').val());
            console.log($('#asunto').val());
            console.log($('#mensaje').val());
            $.ajax({
                type:'post',
                url: '/enviarMensajeInstitucion/',
                data:{
                    'emisor':usuario,
                    'destinatario':$('#destinatario').val(),
                    'asunto':$('#asunto').val(),
                    'mensaje':$('#mensaje').val(),
                    'csrfmiddlewaretoken' : $.cookie('csrftoken')
                },
                beforeSend: function(){
                    bloquearBotones();
                    $('#btn_enviar_mensaje_nuevo').attr('disabled',true);
                    limpiarInputsMensajes();
                },
                success: function (data) {
                    var objeto = JSON.parse(data);
                    console.log(objeto.save_estado);
                    if(objeto.save_estado){
                        console.log('dentro de mensaje enviado exitosamente');
                        $('#info_mensaje_enviado').removeClass('alert-danger');
                        $('#info_mensaje_enviado').show();
                        var html = "<strong><p><span class='glyphicon glyphicon-ok-sign'></span>Mensaje Enviado Exitosamente</p></strong>";
                        $('#info_mensaje_enviado').addClass('alert alert-success');
                        $('#info_mensaje_enviado_txt').html(html);
                        buzonSalidaInstitucion();
                    }else{
                        $('#info_mensaje_enviado').removeClass('alert-success');
                        $('#info_mensaje_enviado').show();
                        var html = "<strong><p><span class='glyphicon glyphicon-exclamation-sign'></span>Error al enviar mensaje</p></strong>";
                        $('#info_mensaje_enviado').addClass('alert alert-danger');
                        $('#info_mensaje_enviado_txt').html(html);
                        nuevoMensajeInstitucion();
                    }
                },
                complete: function(){
                    desbloquearBotones();
                    $('#btn_enviar_mensaje_nuevo').attr('disabled',false);
                }
            })
        });


