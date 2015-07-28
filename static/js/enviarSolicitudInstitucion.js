$("#enviarSolicitud").click(function () {
	console.log($("#siglas_institucion").val());
	$.ajax({
		  type: "POST",
		  url: "/envioSolicitud",
		  data: {
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
				'siglas_institucion' : $("#siglas_institucion").val()
		  },
		  success: solicitudSuccess,
		  dataType: 'html'
	});
	console.log('bye');
});

function solicitudSuccess(data, textStatus, jqXHR){
	$("#formPeticion").html(data);
	$("#siglas_institucion").val("");
}