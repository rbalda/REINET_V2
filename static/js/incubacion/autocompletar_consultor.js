/**
 * Created by Ray on 18/08/2015.
 */
$(function() {
  $("#destinatario_txt").autocomplete({
    source: "/AutocompletarConsultor",
    minLength:2,
    labels: ["first_name"]
  });
});

  $('#formulario').on('keyup change click',function(){

    var nameVal = $('#destinatario_txt').val()

    var nameLength = nameVal.length;

    var nameSplit = nameVal.split('-');

    var lastLength = nameLength - nameSplit[0].length;

    var lastNameLength = nameSplit[0].length + lastLength;

    var lastName = nameVal.slice(lastNameLength);

    if (existeDivision()){
        $('#destinatario').val(nameSplit[1]);
    }else{destinatario
        $('#destinatario').val(nameVal);
    }


  });


function existeDivision(){
    var nameVal = $('#destinatario_txt').val()

    var nameLength = nameVal.length;

    var nameSplit = nameVal.split('-');

    var lastLength = nameLength - nameSplit[0].length;

    var lastNameLength = nameSplit[0].length + lastLength;

    var lastName = nameVal.slice(lastNameLength);

    if(nameSplit.length >1){
        return true;
    }else{
        return false;
    }

}