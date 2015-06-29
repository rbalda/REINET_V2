var redInn = angular.module('redInn',['ngResource','ngAnimate','ngRoute','ngCookies','SwampDragonServices']);

//Configuracion de angular para que no se confunda con sintaxis django
redInn.config(['$interpolateProvider','$resourceProvider',function( $interpolateProvider,$resourceProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

//Agregando csrf token en cada peticion ajax que realice angular
redInn.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

//definiendo urls contantes
redInn.constant('urls', {
       BASE: '/',
       BASE_API: '/api'
});


//Creando servicio para busqueda de entidades en la barra de busquedas
redInn.factory('Entidades',['$http','urls',function($http,urls){
    return{
        get_usuarios: function (data, success, error) {
            $http.get(urls.BASE_API + '/buscar_usuario/?busqueda='+ data, {},
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

//controlador que hara la busqueda de los usuario y los mostrara en pantalla
redInn.controller('ControladorBusqueda',['$scope','Entidades',function($scope,Entidades){
    $scope.busqueda_entrada = null;
    $scope.lista_usuarios = [];
    $scope.lista_instituciones = [];
    $scope.esta_vacio = function(){
        return ($scope.no_usuarios()&&$scope.no_instituciones());
    }

    $scope.no_usuarios = function(){
        if($scope.lista_usuarios.length<1){
            return true;
        }
        else{
            return false;
        }
    }

    $scope.no_instituciones = function(){
        if($scope.lista_instituciones.length<1){
            return true;
        }
        else{
            return false;
        }
    }

    $scope.buscar_entidades = function(){
        Entidades.get_usuarios($scope.busqueda_entrada,
            function(respuesta){
                $scope.lista_usuarios=respuesta;
            },
            function () {
                $log('No encontrado');
            });
        Entidades.get_instituciones($scope.busqueda_entrada,
            function(respuesta){
               $scope.lista_instituciones=respuesta;
            },
            function(){
                $log('No encontrado')
            });

        if ($scope.busqueda_entrada ===''){
            $scope.lista_usuarios = [];
            $scope.lista_instituciones = [];
        }
    }
}]);


redInn.controller('MensajesControllers',['$scope','$dragon',function($scope,$dragon){
    $scope.mensaje = {};
    $scope.mensajes = [];
    $scope.channel = 'mensaje';
    $scope.nroMensajes=0;



    $dragon.onReady(
        function(){
            $dragon.subscribe('mensaje-router',$scope.channel,{}).then(function(response){
                    $scope.dataMapper = new DataMapper(response.data);
                });
            $dragon.getSingle('mensaje-router',{id:1}).then(function(response){
                $scope.mensaje = response.data;
            });
            $dragon.getList('mensaje-router',{leido:false}).then(function (response) {
                $scope.mensajes = response.data;
            });

        });

    $dragon.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                $scope.dataMapper.mapData($scope.mensajes, message);
            });
        }
    });
//    $dragon.onChannelMessage(function(channels, message) {
//    if (indexOf.call(channels, $scope.channel) > -1) {
//        this.dataMapper.mapData($scope.todoItems, message);
//        $scope.$apply();
//    }
//});

}]);