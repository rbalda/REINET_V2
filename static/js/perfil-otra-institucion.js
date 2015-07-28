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

    	$('#btn_sucribirte').css('font-weight', 'bold');


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
	            console.log('misma_institucion'+misma_institucion);
	            if (misma_institucion==false && es_afiliado == true){
	            	console.log('misma institucion false');
					$('#btn_sucribirte').attr('disabled', true);

    			}else if(misma_institucion==true || es_afiliado==false){
    				console.log('misma institucion true');
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
		                  switch(objeto.estadoMembresia){
		                      case -1:
		                      //si existe membresia pero fue rechazado
		                        $('#btn_sucribirte').attr('disabled', false);
		                      break;
		                      case 0:
		                      //si existe membresia pendiente de accion
		                      	$('#btn_sucribirte').attr('disabled', true);
		                      	$('#btn_sucribirte').css('color', 'blue');
		                        var html = "Usted ya ha enviado una solicitud"
		                        $('#btn_sucribirte').text(html);
		                        
		                      break;
		                      case 1:
		                      //si existe membresia aceptada
		                      	$('#btn_sucribirte').attr('disabled', true);
		                      	$('#btn_sucribirte').css('color', 'blue');
		                        var html = "Usted ya pertenece a esta Institución"
		                        $('#btn_sucribirte').text(html);
		                      break;
		                  }
		                }else{
		                  //no existe membresia
		                  $('#btn_sucribirte').attr('disabled', false);
		                }
		              }
		            });
				//fin de else es_afiliado
    			}
	        });
	    });
    });

$(document).on('click','#btn_aceptar_Suscripcion',function(){
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
                  var objeto = JSON.parse(data);
                  console.log('aqui se imprime el objeto')
                  console.log(objeto);
                  if (objeto.save_estado){
                  	$('#btn_sucribirte').attr('disabled', true);
                  	$('#btn_sucribirte').popover('hide');
                  	$('#btn_sucribirte').text("Solicitud Enviada");
                  	$('#btn_sucribirte').css('color', 'blue');

                  	var html = '<p><span class="glyphicon glyphicon-ok-sign"></span> Se ha enviado la solicitud</p>';
                    $('#info_suscripcion').addClass("alert alert-info");
                    $('#info_suscripcion_txt').html(html);
                    $('#info_suscripcion').removeClass("alert-warning");
                    $('#info_suscripcion').show();
                  }else{
                  	var html = '<p><span class="glyphicon glyphicon-exclamation-sign"></span> Error inesperado. <br>Vuelva a intentarlo mas tarde</p>';
                  	$('#info_suscripcion').addClass("alert alert-warning");
                  	$('#info_suscripcion_txt').html(html);
                  	$('#info_suscripcion').show();
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