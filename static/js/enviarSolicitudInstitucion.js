$("#enviarSolicitud").click(function () {
	console.log($("#nombre_institucion").val());
	$.ajax({
		  type: "POST",
		  url: "/envioSolicitud",
		  data: {
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
				'nombre_institucion' : $("#nombre_institucion").val()
		  },
		  success: solicitudSuccess,
		  dataType: 'html'
	});
	console.log('bye');
});

function solicitudSuccess(data, textStatus, jqXHR){
	$("#formPeticion").html(data);
	$("#nombre_institucion").val("");
}