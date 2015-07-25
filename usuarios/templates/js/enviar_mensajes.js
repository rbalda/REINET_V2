$("#enviarMensaje").click(function () {
    console.log($("#destinatario").val());
	$.ajax({
		  type: "POST",
		  url: "/enviarMensaje",
		  data: {
              'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
	          'destinatario' : $("#destinatario").val(),
              'asunto' : $("#asunto").val(),
              'mensaje' : $("#mensaje").val()
		  },
		  success: function solicitudSuccess(data){
                    console.log("olakase");
                    $("#contenidoRetroalimentacion").html(data);
                },
		  dataType: 'html'
	});

});