
var appincubacion = angular.module('redInn');



appincubacion.controller('crearIncubacionFormController',['$scope','$rootScope','Oferta','$timeout','$window',function($scope,$rootScope,Oferta,$timeout,$window){
    // dentro del scope van modelos


    console.log('dentro del crearIncubacionAngular');

    $scope.incubacion = new Oferta();

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_alcance = [{tipo: "Todos", valor: 0 },{tipo: "Grupo", valor: 1 }];

    $scope.tipo = 0;
    $scope.hide = true;
    $scope.validar_form=true;
    $scope.forms = {};
    $scope.imagen = {};


    function isEmpty(myObject) {
        for(var key in myObject) {
            if (myObject.hasOwnProperty(key)) {
                return false;
            }
        }

        return true;
    }


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
    
    $scope.guardar = function(){

        $scope.incubacion.tiempo_para_estar_disponible=tiempo + " " + duracion;

        $scope.incubacion.$save(function(response){
            console.log('Se ha creado con exito la Incubacion');

            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.incubacion = new Oferta();
            $scope.tiempo_tipo="";
            $scope.tiempo_disponible=1;
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


appincubacion.factory('Oferta',['$resource',function($resource){
    return $resource("/api/ofertas/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);


function getQueryVariable(variable, url) {
    var query = url;
    var vars = query.split("page=");
    console.log(query);
    if (vars[1]!=null){
        return vars[1];
    }
    return "1";
}











