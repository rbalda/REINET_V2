
var appoferta = angular.module('redInn');

appoferta.controller('crearOfertaFormController',['$scope','$window' ,'Oferta',function($scope,$window,Oferta){
    // dentro del scope van modelos
    console.log('dentro del crearOfertaAngular');

    $scope.oferta = new Oferta();

    $scope.tabs = ['/static/templates-ofertas-demandas/crear_oferta_form1.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form2.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form3.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form4.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form5.html'];

    $scope.actualtab = 0;
    $scope.tiempo_disponible = 1;
    $scope.hide1 = true;
    $scope.hide2 = true;
    $scope.formActual = $scope.tabs[$scope.actualtab];

    $scope.items_tipo = [{tipo: 'Emprendimiento', valor: 0 },{tipo: 'Tecnolog\u00EDa', valor: 1 },{tipo: 'Prototipo', valor: 2 }];
    $scope.items_date = [{tipo: 'A\u00F1o', valor: 0 },{tipo: 'Mes', valor: 1 }];
    $scope.tipo_oferta = $scope.items_tipo[0];
    $scope.tiempo_oferta = $scope.items_date[0];
  

    $scope.seleccionartab=function(indice){
        $scope.formActual = $scope.tabs[indice];
        $scope.actualtab = indice;
    };

    $scope.siTabEsSeleccionado=function(indice){
        return indice == $scope.actualtab;
    };

    $scope.siguiente = function(){
        $scope.actualtab = $scope.actualtab+1;
        $scope.formActual = $scope.tabs[$scope.actualtab];
    }

    $scope.atras = function(){
        if($scope.actualtab>0)
            $scope.actualtab=$scope.actualtab-1;
         $scope.formActual = $scope.tabs[$scope.actualtab];
    }

    $scope.oferta.tipo =$scope.tipo_oferta.valor;
    $scope.oferta.tiempo_para_estar_disponible = $scope.tiempo_disponible + ' ' + $scope.tiempo_oferta.tipo;

    $scope.guardar = function(){

        $scope.oferta.$save(function(response){
            console.log('Se ha creado con exito la Oferta');
            $window.location.href = '/administrarOferta/';
            $scope.info_crear_oferta_success = "Oferta creada exitosamente";
            $scope.hide1=false;
        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.info_crear_oferta_error = "Hubo un error al crear oferta";
            $scope.hide2=false;

        });
    }

//fin de controller
}]);

appoferta.factory('Oferta',['$resource',function($resource){
    return $resource("http://localhost:8000/api/ofertas/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);















