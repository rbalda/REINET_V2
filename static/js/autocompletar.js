/**
 * Created by Ray on 30/06/2015.
 */
$(function() {
  $("#destinatario").autocomplete({
    source: "/completar_username",
    minLength: 2
  });
});