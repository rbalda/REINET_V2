
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

// directiva para validar fecha de incubacion
appincubacion.directive('validarFecha',function($http){
    return{
        require: 'ngModel', //tipo de target de directiva
        link: function(scope,elem,attr,ctrl){ //funcion que hace el link con la directiva -siempre es igual

            scope.$watch(attr.ngModel, function(value){
                var fecha = new Date(value);
                var fecha_actual = new Date();

                if ( value != undefined){ // que exista fecha en input

                    // fecha menor o igual a hoy, validez del form falso y mostramos mensaje
                    if(fecha < fecha_actual){
                        scope.fecha_incorrecta = true;
                        ctrl.$setValidity('validarFecha',false);

                    // fecha correcta, validez del form true y no mostramos mensaje
                    }else{
                        ctrl.$setValidity('validarFecha',true);
                        scope.fecha_incorrecta = false;
                    };
                };

            });
        }
    }
});









