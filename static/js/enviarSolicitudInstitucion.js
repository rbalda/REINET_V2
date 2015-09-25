$("#enviarSolicitud").click(function () {
	console.log($("#siglas_institucion").val());
	$.ajax({
		  type: "GET",
		  url: "/envioSolicitud",
		  data: {
				//'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
				'nombre_institucion' : $("#siglas_institucion").val(),
		  },
		  success: solicitudInstSuccess,
		  dataType: 'html',
		  async: false,
	});
	console.log('bye');
});

function solicitudInstSuccess(data, textStatus, jqXHR){
	$("#formPeticion").html(data);
	$("#siglas_institucion").val("");
}