/**
 * Created by Ray on 30/06/2015.
 */
$(function() {
  $("#destinatario_txt").autocomplete({
    source: "/AutocompletarUsuario",
    minLength:2,
    labels: [ "first_name"]
  });
});

/**
$("#destinatario_txt").on('change',function(responseText) {
    $.each(responseText.split('-'), function(index, value) {
        if(index == 0){
          $('#nombres').val(value);
        }
        else if(index == 1){
             $('#destinatario').val(value);
        }
    });

});
*/

  $('#destinatario_txt').on('keyup change click',function(){

    var nameVal = $('#destinatario_txt').val()

    var nameLength = nameVal.length;

    var nameSplit = nameVal.split('-');

    var lastLength = nameLength - nameSplit[0].length;

    var lastNameLength = nameSplit[0].length + lastLength;

    var lastName = nameVal.slice(lastNameLength);

    $('#destinatario').val(nameSplit[1]);
  });