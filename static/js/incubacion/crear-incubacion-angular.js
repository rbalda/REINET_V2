
var appincubacion = angular.module('redInn');



appincubacion.controller('crearIncubacionFormController',['$scope','$rootScope','Incubacion','$timeout','$window',function($scope,$rootScope,Incubacion,$timeout,$window){

    // se crea nuevo objeto de incubacion
    $scope.incubacion = new Incubacion();

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_alcance = [{tipo: "Todos", valor: 0 },{tipo: "Grupo", valor: 1 }];
    $scope.hide = true;
    
    // funcion guardar al dar click
    $scope.guardar = function(){
        console.log('click guardar incubacion');

        // funcion save del objeto incubacion
        $scope.incubacion.$save(function(response){

            console.log('Se ha creado con exito la Incubacion');
            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.incubacion = new Incubacion();
            $scope.info_crear_incubacion = "Incubacion creada exitosamente";
            $scope.hide=false; 

        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.textType="alert-danger";
            $scope.iconoClass="glyphicon-exclamation-sign";
            $scope.info_crear_incubacion = "Hubo un error al crear incubacion";
            $scope.hide=false; 

        });
    }

//fin de controller
}]);

// factory para poder usar el api/incubacion
appincubacion.factory('Incubacion',['$resource',function($resource){
    return $resource("/api/incubacion/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);











