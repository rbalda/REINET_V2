var appoferta = angular.module('redInn');

appoferta.controller('verOfertaController',['$scope','Oferta',function($scope,Oferta){
    // dentro del scope van modelos
    console.log('dentro del verOfertaController');
    $scope.NombreOferta = Oferta()


}]);

appoferta.factory('Oferta',['$resource',function($resource){
   return{
        get_usuarios: function (data, success, error) {
            $http.get('api/buscar_usuario/?busqueda='+ data, {},
                {headers: {"Content-Type": "application/json"}
                }).success(success).error(error);
        },
        get_instituciones: function(data, success, error) {
            $http.get(urls.BASE_API + '/buscar_institucion/?busqueda='+ data, {},
                {headers: {"Content-Type": "application/json"}
                }).success(success).error(error);
        }
    }
}]);