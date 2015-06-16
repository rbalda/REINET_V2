var redInn = angular.module('redInn',['ngResource','ngAnimate','ngRoute','ngCookies']);

redInn.config(['$interpolateProvider','$resourceProvider',function( $interpolateProvider,$resourceProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

redInn.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

redInn.constant('urls', {
       BASE: '/',
       BASE_API: '/api'
});

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
