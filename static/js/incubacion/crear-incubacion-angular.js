/* 

Autor: Fausto Mora 
Nombre del Archivo: crear-incubacion-angular.js
Descripción: script hecho en angular que controla todo lo relacionado
con crear incubacion

*/


var appincubacion = angular.module('redInn');

appincubacion.controller('crearIncubacionFormController',['$scope','$rootScope','Incubacion','$timeout','$window',function($scope,$rootScope,Incubacion,$timeout,$window){

    // se crea nuevo objeto de incubacion
    $scope.incubacion = new Incubacion();
    $scope.incubacion_id = null;
    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_alcance = [{tipo: "Todos", valor: 0 },{tipo: "Grupo", valor: 1 }];
    $scope.hide = true;
    

    // codigo para hacer modal
    $scope.showModal = false;

    // funcion guardar al dar click
    $scope.guardar = function(){
        console.log('click guardar incubacion');

        // funcion save del objeto incubacion
        $scope.incubacion.$save(function(response){

            console.log('Se ha creado con exito la Incubacion');
            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.info_crear_incubacion = "Incubacion creada exitosamente";

            var id = $scope.incubacion.id_incubacion;
            $scope.incubacion_id = id;

            $scope.incubacion = new Incubacion();
            
            $scope.showModal = !$scope.showModal;


            $scope.redirectIncubacion = function (){
                window.location.replace( "/AdminIncubacion/"+id);
            }

        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.exito_creacion=false; 
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
                var fecha = new Date(value); // crea fecha del input date
                var fecha_actual = new Date(); // crea fecha actual

                if ( value != undefined){ // que exista fecha en input

                    // fecha menor o igual a hoy, validez del form falso y mostramos mensaje
                    if(fecha < fecha_actual && !compararFechas(fecha,fecha_actual)){
                        scope.fecha_incorrecta = true;
                        ctrl.$setValidity('validarFecha',false);

                    // fecha correcta, validez del form true y no mostramos mensaje
                    }else{
                        ctrl.$setValidity('validarFecha',true);
                        scope.fecha_incorrecta = false;
                    };
                };

            });

            // funcion para determinar si son fechas exactamente iguales
            function compararFechas(fecha1,fecha2){
                if(fecha1.getFullYear() == fecha2.getFullYear()){
                    if(fecha1.getMonth() == fecha2.getMonth()){
                        if(fecha1.getDate() == fecha2.getDate()){
                            return true;
                        };
                    };
                };
                return false;
            };

        }
    }
});


// directiva para el modal al exito de la creacion de una incubacion
appincubacion.directive('modal', function () {
    return {
        // template del modal a renderizarse
      template: '<div class="modal fade">' + 
          '<div class="modal-dialog">' + 
            '<div class="modal-content">' + 
              '<div class="modal-header">' +
                '<div class="col-md-offset-2">'+
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' + 
                '<div ng-transclude></div>' +
                '</div>' +
              '</div>' + 
              '<div class="modal-body" style="height:74px;">' +
              '<div class="col-md-10 col-md-offset-2">'+
                '<button type="button" ng-click="redirectIncubacion()" class="btn btn-red pull-right" style="margin:4px; width:60px;">Ver</button>'+
                '<a class="btn btn-dark pull-right" style="margin:4px;" data-dismiss="modal"><i class="fa fa-times"></i>&nbsp;&nbsp;Cancelar&nbsp;&nbsp;</a>'+
              '</div>'+
              '</div>'+
            '</div>' + 
          '</div>' + 
        '</div>',
        //propiedades para el modal
      restrict: 'E',
      transclude: true,
      replace:true,
      scope:true,
      link: function postLink(scope, element, attrs) { //funcion que hace el link con la directiva

        scope.$watch(attrs.visible, function(value){ //funcion watch para vigilar el scope de la directiva
            // si value es verdadero se muestra el modal
          if(value == true){
            $(element).modal('show');
          }else{ //caso contrario se oculta
            $(element).modal('hide');
          }
        });

        $(element).on('shown.bs.modal', function(){ //funcion para presentar el modal
          scope.$apply(function(){
            scope.$parent[attrs.visible] = true;
          });
        });

        $(element).on('hidden.bs.modal', function(){ //funcion para ocultar el modal
          scope.$apply(function(){
            scope.$parent[attrs.visible] = false;
          });
        });
      }
    };
  });