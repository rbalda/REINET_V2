$('#instBtnContinuar').click(function(){
    console.log('hi im here');
    console.log($('#codigoInstitucion').val());
    $.ajax({
      type: "POST",
      url: "/ver_codigo",
      data: {
          'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
          'codigo' : $('#codigoInstitucion').val()
      },
      success: codeSuccess,
      dataType: 'html'
    });
});

function codeSuccess(data, textStatus, jqXHR){
    $('#formulario').append(data);
    $('#codigoInstitucion').remove();
    $('#instBtnContinuar').remove();
}

