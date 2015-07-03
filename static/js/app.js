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


redInn.factory('ContarNoLeidos',['$http','urls',function($http,urls){
    return{
        get_contador: function (success, error) {
            $http.get(urls.BASE_API + '/contar_no_leidos', {},
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


redInn.controller('MensajesControllers',['$scope','$dragon','$rootScope',function($scope,$dragon,$rootScope){
    $scope.mensaje = {};
    $scope.mensajes = [];
    $scope.channel = 'mensaje';
    $scope.nroMensajes=0;
    $scope.mostrarNotificacion = false;

    var notificar = function(){
        $scope.mostrarNotificacion=true;
        setTimeout(function () {
                $scope.$apply(function(){
                    $scope.mostrarNotificacion=false;
                });
            },8000);
    };

    var usuarioName = function(){
        var temp = angular.element('#usuario').children();
        return temp[0].text.replace(/\n/g,'').replace(/ /g,'');
    };

    var obtenerNuevoMensaje = function(){

    };

    $dragon.onReady(
        function(){
            $dragon.subscribe('mensaje-router',$scope.channel,{fk_receptor__username:usuarioName()}).then(function(response){
                    $scope.dataMapper = new DataMapper(response.data);
                });
            $dragon.getSingle('mensaje-router',{username:usuarioName()}).then(function(response){
                $scope.mensaje = response.data;
            });
        });

    $dragon.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                $scope.dataMapper.mapData($scope.mensajes, message);
                if(message.action=='created'){
                    notificar();

                }
                $rootScope.$broadcast('actualizar-mensajes');
            });
        }
    });

}]);

redInn.controller('MensajesContadorController',['$scope','ContarNoLeidos',function($scope,ContarNoLeidos){
    $scope.contador=null;

    var contar = function(){
        ContarNoLeidos.get_contador(
            function(response){
                $scope.contador=response;
            }
        );
    };

    contar();

    $scope.$on('actualizar-mensajes',
        function(){
            contar();
        }
    );

}]);



/// Controlador de Notificaciones 
/// Modf:Usado para notificar accion de membresias - Fausto Mora

redInn.controller('NotificacionControllers',['$scope','$dragon','$rootScope',function($scope,$dragon,$rootScope){
    //$scope.mensaje = {};
    $scope.notificacion = [];
    $scope.channel = 'notificacion';
    $scope.nroNotificacion=0;
    $scope.mostrarNotificacion = false;

    var notificar = function(){
        $scope.mostrarNotificacion=true;
        setTimeout(function () {
                $scope.$apply(function(){
                    $scope.mostrarNotificacion=false;
                });
            },8000);
    };

    var usuarioName = function(){
        var temp = angular.element('#usuario').children();
        return temp[0].text.replace(/\n/g,'').replace(/ /g,'');
    };

    $dragon.onReady(
        function(){
            $dragon.subscribe('notificacion-router',$scope.channel,{fk_receptor__username:usuarioName()}).then(function(response){
                    $scope.dataMapper = new DataMapper(response.data);
                });
            $dragon.getSingle('notificacion-router',{username:usuarioName()}).then(function(response){
                $scope.mensaje = response.data;
            });
        });

    $dragon.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                $scope.dataMapper.mapData($scope.mensajes, message);
                if(message.action=='created'){
                    notificar();

                }
                $rootScope.$broadcast('actualizar-notificacion');
            });
        }
    });

}]);

redInn.controller('NotificacionContadorController',['$scope','ContarNoLeidos',function($scope,ContarNoLeidos){
    $scope.contador_notificacion=null;

    var contar = function(){
        ContarNoLeidos.get_contador(
            function(response){
                $scope.contador_notificacion=response;
            }
        );
    };

    contar();

    $scope.$on('actualizar-notificacion',
        function(){
            contar();
        }
    );

}]);