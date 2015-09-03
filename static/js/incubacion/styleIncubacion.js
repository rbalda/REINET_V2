$(function () {
  $('#popoverDescripcion').popover({
  	html : true,
  	content:function() {
      return $('#retroalDescripcion').html();
    }
  });
});