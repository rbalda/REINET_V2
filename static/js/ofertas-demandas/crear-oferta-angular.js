
var appoferta = angular.module('redInn');

appoferta.controller('crearOfertaFormController',['$scope','$rootScope','Oferta','$timeout',function($scope,$rootScope,Oferta,$timeout){
    // dentro del scope van modelos


    console.log('dentro del crearOfertaAngular');

    $scope.oferta = new Oferta();

    $scope.tabs = ['/static/templates-ofertas-demandas/crear_oferta_form1.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form2.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form3.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form4.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form5.html'];

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_date = [{tipo: "A\u00F1o", valor: 0 },{tipo: "Mes", valor: 1 }];

    $scope.actualtab = 0;
    $scope.tipo = 0;
    $scope.hide = true;
    $scope.validar_form=true;
    $scope.formActual = $scope.tabs[$scope.actualtab];
    $scope.forms = {};

    var tiempo='1';
    var duracion='A\u00F1o';

    $scope.validarSubmit = function(form1){
        console.log('dentro validarSubmit');
        if(form1===undefined){
            console.log('form undefined');
        }else{
            console.log('form defined');
             if(form1.$valid){
                console.log('form valido');
                $rootScope.$broadcast('elformesvalido');
            }else{
                console.log('form invalido');
                $scope.validar_form=true; 
            }
        }
    };

    $scope.$on('elformesvalido',function(){
        $scope.validar_form=false;
    });

    $scope.tiempoDisponibleSelect = function(val){
        if(val===undefined){
            console.log('no tiempoDisponibleSelect val');
        }else{
            console.log(val);
            duracion=val;
        }
    };

    $scope.tiempoDisponibleInput = function(val){
        if(val===undefined){
            console.log('no tiempoDisponibleInput val');
        }else{
            console.log(val);
            tiempo=val;
        }
    };
    
  
    
    $scope.seleccionartab=function(indice){
        console.log('dentro de seleccionartab')
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

    $scope.guardar = function(){
        $scope.oferta.tiempo_para_estar_disponible=tiempo + " " + duracion;

        $scope.oferta.$save(function(response){
            console.log('Se ha creado con exito la Oferta');
            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.oferta = "";
            $scope.oferta = new Oferta();
            $scope.tiempo_tipo="";
            $scope.tiempo_disponible=1;
            $scope.info_crear_oferta = "Oferta creada exitosamente";
            $scope.hide=false;
            $scope.actualtab = 0;
            $scope.formActual = $scope.tabs[0];
            
        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.textType="alert-danger";
            $scope.iconoClass="glyphicon-exclamation-sign";
            $scope.info_crear_oferta = "Hubo un error al crear oferta";
            $scope.hide=false;

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


//appoferta.directive('ngUpdateHidden',function() {
//    return function(scope, el, attr) {
//        var model = attr['ngModel'];
//        scope.$watch(model, function(nv) {
//            console.log(el.val(nv));
//        });
//
//    };
//});











