/*
 * Autor: Fausto Mora
 Nombre de función: script para el perfil de otra institucion
 Salida: 
 Descripción: permite la interaccion de la vista desde una institucion 
 con el usuario al momento de enviar solicitud para membresia
*/

    $(document).ready(function () {
    	console.log($('#inst_value').val());

    	$.getScript("/static/js/jquery.cookie.js", function(){

		});

        $('#btn_sucribirte').popover({
            html: true,
            content: function () { 
                return $('#popover_content_wrapper').html();
            }
        });

        $(function(){
	        $('#info_suscripcion').removeClass("alert alert-info alert-warning");
	        $('#info_suscripcion').hide();
	        $('#btn_sucribirte').ready(function (){
	            console.log('dentro de la verificacion');
	            $.ajax({
	              data:{
	                'institucion':$('#inst_value').val()
	              },
	              type:'get',
	              url: '/verificarSuscripcion/',
	              success: function(data){
	                var objeto = JSON.parse(data);
	                console.log(objeto);
	                if (objeto.existeMembresia) {
	                  $('#btn_sucribirte').hide();
	                  $('#info_suscripcion').show();
	                  switch(objeto.estadoMembresia){
	                      case -1:
	                      //si existe membresia pero fue rechazado
	                        $('#btn_sucribirte').show();
	                        $('#info_suscripcion').hide();
	                      break;
	                      case 0:
	                      //si existe membresia pendiente de accion
	                        var html = "<p>Usted ya ha enviado una solicitud</p>"
	                        $('#info_suscripcion').addClass("alert alert-warning");
	                        $('#info_suscripcion').removeClass("alert-info");
	                      break;
	                      case 1:
	                      //si existe membresia aceptada
	                        var html = "<p>Usted ya pertenece a esta Institucion</p>"
	                        $('#info_suscripcion').addClass("alert alert-info");
	                        $('#info_suscripcion').removeClass("alert-warning");
	                      break;
	                  }
	                }else{
	                  //no existe membresia
	                  $('#btn_sucribirte').show();
	                  $('#info_suscripcion').hide();
	                }
	                
	                $('#info_suscripcion').html(html);
	              }
	            });
	        });
	    });
    });

$(document).on('click','#btn_aceptar_Suscripcion',function(){
    //alert($('#txt_cargo').val());
    console.log('dentro de suscribirAInstitucion');
    console.log($('#txt_cargo').val());
    console.log($('#txt_description').val())
    var formularioValido=validarSolicitud();
    if(formularioValido == true){
      $.ajax({
          data: {
          'cargo':$('#txt_cargo').val(),
          'descripcion':$('#txt_description').val(),
          'institucion' : $('#inst_value').val(),
          'csrfmiddlewaretoken' : $.cookie('csrftoken')
          },
          type: 'post',
          url: '/suscribirAInstitucion/',
          success: function(data){
                  var html = "<p>Se ha enviado la solicitud</p>";
                  var objeto = JSON.parse(data);
                  console.log('aqui se imprime el objeto')
                  console.log(objeto);
                  if (objeto.save_estado){
                    $('#info_suscripcion').addClass("alert alert-success");
                    $('#info_suscripcion').html(html);
                    $('#info_suscripcion').removeClass("alert-info");
                    $('#info_suscripcion').removeClass("alert-warning");
                    $('#btn_sucribirte').popover('hide');
                    $('#btn_sucribirte').hide();
                    $('#info_suscripcion').show();
                  }else{
                  	$('#info_suscripcion').addClass("alert alert-warning");
                  	$('#info_suscripcion').html("<p>Error inesperado</p>");
                  }
          }
      });
    }

    function validarSolicitud()
      {
        var cargo = $('#txt_cargo').val();
        var descripcion = $('#txt_description').val();
        var patroncargo = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
        var patrondescripcion = /^[_\-.,;a-z0-9A-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
        var resultado1 = patroncargo.test(cargo);
        var resultado2 = patrondescripcion.test(descripcion);
        if(resultado1 == false)
        {
          $('#errorCargo').css("display","block");
        }
        else
        {
          $('#errorCargo').css("display","none");
        }
        if(resultado2 == false)
        {
          $('#errorDescripcion').css("display","block");
        }
        else
        {
          $('#errorDescripcion').css("display","none");
        }
        //alert('cargo: ' + resultado1 + ' descripcion '+ resultado2);
        return resultado1 && resultado2;
      }

  });


/* fin de script */