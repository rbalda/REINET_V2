
var appincubacion = angular.module('redInn');



appincubacion.controller('crearIncubacionFormController',['$scope','$rootScope','Incubacion','$timeout','$window',function($scope,$rootScope,Incubacion,$timeout,$window){
    // dentro del scope van modelos

    console.log('dentro del crearIncubacionAngular');

    $scope.incubacion = new Incubacion();

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_alcance = [{tipo: "Todos", valor: 0 },{tipo: "Grupo", valor: 1 }];
    $scope.hide = true;
    
    $scope.guardar = function(){
        console.log('click guardar incubacion');

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


appincubacion.factory('Incubacion',['$resource',function($resource){
    return $resource("/api/incubacion/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);











