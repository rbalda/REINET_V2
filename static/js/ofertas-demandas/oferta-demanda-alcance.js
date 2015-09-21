var appalcance = angular.module('redInn');

appalcance.controller();


appdemanda.controller('AlcanceController',['$scope','$http','urls',function($scope,$http,urls){
	console.log('dentro de alcance');
    $scope.listaInstituciones = [];

    $http.get(urls.BASE_API+'/alcance/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
    	console.log('dentro de lista get');
        $scope.lista = response.results;
    }).error(function(){
        console.log('hubo un error en select demandas');
    });

	$scope.loadInstituciones = function($query) {
		console.log('dentro de loadInstituciones');
	return $http.get(urls.BASE_API+'/alcance/', { cache: true}).then(function(response) {
	  var instituciones = response.data;
	  return instituciones.filter(function(item) {
	    return item.siglas.toLowerCase().indexOf($query.toLowerCase()) != -1;
	  });
	});
	};

    
}]);