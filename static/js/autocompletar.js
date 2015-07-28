/**
 * Created by Ray on 30/06/2015.
 */
$(function() {
  $("#destinatario").autocomplete({
    source: "/AutocompletarUsuario",
    minLength:2,
    labels: [ "first_name"]
  });
});