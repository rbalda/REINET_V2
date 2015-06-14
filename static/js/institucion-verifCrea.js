$('#instBtnContinuar').click(function(){
    $.ajax({
      type: "POST",
      url: "/verificar_codigo",
      data: {
          'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
          'codigo' : $('#codigoInstitucion').val()
      },
      success: codeSuccess,
      dataType: 'html'
    });
});

function codeSuccess(data, textStatus, jqXHR){
    $('#formulario').html(data);
    $('#codigoInstitucion').remove();
    $('#instBtnContinuar').remove();
}

