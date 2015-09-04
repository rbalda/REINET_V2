$(function () {
  $('#popoverDescripcion').popover({
  	html : true,
  	content:function() {
      return $('#retroalDescripcion').html();
    }
  });
});

$(function () {
  $('#popoverPerfilCliente').popover({
  	html : true,
  	content:function() {
      return $('#retroalPerfilCliente').html();
    }
  });
});

$(function () {
  $('#popoverPerfilBeneficiario').popover({
  	html : true,
  	content:function() {
      return $('#retroalPerfilBeneficiario').html();
    }
  });
});

$(function () {
  $('#popoverSocioClave').popover({
  	html : true,
  	content:function() {
      return $('#retroalSocioClave').html();
    }
  });
});

$(function () {
  $('#popoverActividadesClaves').popover({
  	html : true,
  	content:function() {
      return $('#retroalActividadesClaves').html();
    }
  });
});

$(function () {
  $('#popoverPropuestaValor').popover({
  	html : true,
  	content:function() {
      return $('#retroalPropuestaValor').html();
    }
  });
});


$(function () {
  $('#popoverRelacionesCliente').popover({
  	html : true,
  	content:function() {
      return $('#retroalRelacionesCliente').html();
    }
  });
});

$(function () {
  $('#popoverSegmentosClientes').popover({
  	html : true,
  	content:function() {
      return $('#retroalSegmentosClientes').html();
    }
  });
});


$(function () {
  $('#popoverRecursosClaves').popover({
  	html : true,
  	content:function() {
      return $('#retroalRecursosClaves').html();
    }
  });
});

$(function () {
  $('#popoverCanales').popover({
  	html : true,
  	content:function() {
      return $('#retroalCanales').html();
    }
  });
});


$(function () {
  $('#popoverEstructurasCostos').popover({
  	html : true,
  	content:function() {
      return $('#retroalEstructurasCostos').html();
    }
  });
});

$(function () {
  $('#popoverFuentesIngresos').popover({
  	html : true,
  	content:function() {
      return $('#retroalFuentesIngresos').html();
    }
  });
});

$(function () {
  $('#popoverTendenciasRelevantes').popover({
  	html : true,
  	content:function() {
      return $('#retroalTendenciasRelevantes').html();
    }
  });
});


$(function () {
  $('#popoverAlternativasSolucionExistentes').popover({
  	html : true,
  	content:function() {
      return $('#retroalAlternativasSolucionExistentes').html();
    }
  });
});

$(function () {
  $('#popoverCompetidores1').popover({
  	html : true,
  	content:function() {
      return $('#retroalCompetidores1').html();
    }
  });
});

$(function () {
  $('#popoverCompetidores2').popover({
  	html : true,
  	content:function() {
      return $('#retroalCompetidores2').html();
    }
  });
});

$(function () {
  $('#popoverPoderConsumidores').popover({
  	html : true,
  	content:function() {
      return $('#retroalPoderConsumidores').html();
    }
  });
});

$(function () {
  $('#popoverSustitutos').popover({
  	html : true,
  	content:function() {
      return $('#retroalSustitutos').html();
    }
  });
});


$(function () {
  $('#popoverPoderProveedores').popover({
  	html : true,
  	content:function() {
      return $('#retroalPoderProveedores').html();
    }
  });
});

$(function () {
  $('#popoverNuevosEntrantes').popover({
  	html : true,
  	content:function() {
      return $('#retroalNuevosEntrantes').html();
    }
  });
});

$(function () {
  $('#popoverEstadoProductoServicio').popover({
  	html : true,
  	content:function() {
      return $('#retroalEstadoProductoServicio').html();
    }
  });
});

$(function () {
  $('#popoverEstrategiaCrecimiento').popover({
  	html : true,
  	content:function() {
      return $('#retroalEstrategiaCrecimiento').html();
    }
  });
});


$(function () {
  $('#popoverEstadoPropiedadIntelectual').popover({
  	html : true,
  	content:function() {
      return $('#retroalEstadoPropiedadIntelectual').html();
    }
  });
});

$(function () {
  $('#popoverEvidenciaTraccion').popover({
  	html : true,
  	content:function() {
      return $('#retroalEvidenciaTraccion').html();
    }
  });
});

$('#btn_rechazada').click(function(e){
        e.preventDefault();
        $('#ofertaRechazada').modal('hide');
        var btn_rechazar =  $('#btn_rechazar_oferta');
        var btn_ver =  $('#btn_ver_oferta');
        var btn_aceptar =  $('#btn_aceptar_oferta');
        btn_aceptar.hide();
        btn_ver.hide();
        btn_rechazar.removeAttr('data-target');
        btn_rechazar.empty();
        btn_rechazar.html('Oferta Rechazada');
        btn_rechazar.removeClass();
        btn_rechazar.toggleClass('btn btn-green');
        btn_rechazar.css('cursor','not-allowed');
});

$('#btn_aceptada').click(function(e){
        e.preventDefault();
        $('#ofertaAceptada').modal('hide');
        var btn_aceptar =  $('#btn_aceptar_oferta');
        var btn_rechazar =  $('#btn_rechazar_oferta');
        
        btn_rechazar.hide();
        btn_aceptar.removeAttr('data-target');
        btn_aceptar.empty();
        btn_aceptar.html('Oferta Aceptada');
        btn_aceptar.removeClass();
        btn_aceptar.toggleClass('btn btn-green');
        btn_aceptar.css('cursor','not-allowed');
});

$('#btn_convocatoria').click(function(e){
        e.preventDefault();
        $('#CrearConvocatoria').modal('hide');
        var btn_participar =  $('#btn_participar');
        btn_participar.removeAttr('data-target');
        btn_participar.empty();
        btn_participar.html('Convocatoria creada');
        btn_participar.removeClass();
        btn_participar.toggleClass('btn btn-green-disable btn-sm');
        btn_participar.css('cursor','not-allowed');
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        var max = new Date($('#fecMaxAlcance').val());
        var timeDiff = Math.abs(today.getTime() - max.getTime());
        var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
        console.log(diffDays);
        if (diffDays>0){
          var btn_participar =  $('#btn_participar');
          btn_participar.removeAttr('data-target');
          btn_participar.empty();
          btn_participar.html('Convocatoria terminada');
          btn_participar.removeClass();
          btn_participar.toggleClass('btn btn-green-disable btn-sm');
          btn_participar.css('cursor','not-allowed');
        }
});

