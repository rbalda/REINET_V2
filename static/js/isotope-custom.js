/*------------------------------------------------------------------
Project:	HighLand
Version:	1.3
Created: 		18/10/2013
Last change:	04/01/2014
-------------------------------------------------------------------*/

// Isotop Gallery 
// ==============

// Layout
$('#isotope-container').isotope({
	// options
	itemSelector : '.isotope-item',
	layoutMode : 'fitRows'
});

// Filtering
var $container = $('#isotope-container');
	$container.isotope({
});
$('#filters a').click(function(){
	var selector = $(this).attr('data-filter');
	$container.isotope({ filter: selector });
	return false;
});