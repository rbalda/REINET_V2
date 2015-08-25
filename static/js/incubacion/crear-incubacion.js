
var appoferta = angular.module('redInn');

appoferta.controller('crearIncubacionFormController',['$scope','$rootScope','Oferta','$timeout','$window',function($scope,$rootScope,Incubacion,$timeout,$window){
    // dentro del scope van modelos


    console.log('dentro del crearIncubacionAngular');

    $scope.oferta = new Incubacion();
    $scope.copia_oferta = $window.oferta_copia;
    $scope.copia_tags = $window.tags_copia;

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_alcance = [{tipo: "Propia institucion", valor: 0 },{tipo: "Grupo", valor: 1 },{tipo: "Todos", valor: 2 }];
    $scope.items_date = [{tipo: "A\u00F1o", valor: 0 },{tipo: "Mes", valor: 1 }];

    $scope.tipo = 0;
    $scope.hide = true;
    $scope.validar_form=true;
    $scope.forms = {};

    function isEmpty(myObject) {
        for(var key in myObject) {
            if (myObject.hasOwnProperty(key)) {
                return false;
            }
        }
        return true;
    }
    var tags={};
    $scope.$watch('incubacion.tags',function(palabra){
        console.log('dentro de watch palabras_clave');
        console.log(palabra);
        tags = palabra;

        if(!isEmpty(tags)){
            console.log('tags'+tags);
            console.log(tags);
            $scope.oferta.tags = tags;
        }
    });


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

        $scope.oferta.$save(function(response){
            console.log('Se ha creado con exito la Incubacion');

            var id = $scope.oferta.id_oferta;
            loadImagen(id);

            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.oferta = new Oferta();
            $scope.tiempo_tipo="";
            $scope.tiempo_disponible=1;
            $scope.info_crear_incubacion = "Incubaci&oacute;n creada exitosamente";
            $scope.hide=false;          
        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.textType="alert-danger";
            $scope.iconoClass="glyphicon-exclamation-sign";
            $scope.info_crear_incubacion = "Hubo un error al crear oferta";
            $scope.hide=false;

        });
    }



//fin de controller
}]);


appoferta.factory('Incubacion',['$resource',function($resource){
    return $resource("/api/incubaciones/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);

/*function getQueryVariable(variable, url) {
    var query = url;
    var vars = query.split("?");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    } 
    return "1";
}*/

function getQueryVariable(variable, url) {
    var query = url;
    var vars = query.split("page=");
    console.log(query);
    if (vars[1]!=null){
        return vars[1];
    }
    return "1";
}

appoferta.controller('CargarOfertasSelectController',['$scope','$http','urls',function($scope,$http,urls){
    $http.get(urls.BASE_API+'/misOfertasAll/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.listaOfertas = response.results;
    }).error(function(){
        console.log('hubo un error en select Ofertas');
    });

    $scope.selectOfertas = function(item){
        console.log(item);
    }
    
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
