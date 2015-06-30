/**
 * Created by Ray on 30/06/2015.
 */
$(function() {
  $("#destinatario").autocomplete({
    source: "/AutocompletarUsuario",
    minLength:3,
    labels: [ "username"]
  });
});