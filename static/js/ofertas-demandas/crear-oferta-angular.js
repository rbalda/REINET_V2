
var appoferta = angular.module('redInn');

appoferta.controller('crearOfertaFormController',['$scope','$window','Oferta',function($scope,$window,Oferta){
    // dentro del scope van modelos
    console.log('dentro del crearOfertaAngular');

    $scope.oferta = new Oferta();

    $scope.tabs = ['/static/templates-ofertas-demandas/crear_oferta_form1.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form2.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form3.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form4.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form5.html'];

    $scope.actualtab = 0;
    $scope.tipo = 0;
    $scope.hide = true;
    $scope.formActual = $scope.tabs[$scope.actualtab];


    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_date = [{tipo: "A\u00F1o", valor: 0 },{tipo: "Mes", valor: 1 }];
  
    /*
    $scope.seleccionartab=function(indice){
        console.log('dentro de seleccionartab')
        console.log(indice)
        var aux = false;
        var aux2 = false;
        var aux3 = false;
        switch(indice){
            case 1:
            console.log('dentro de case 1')
            console.log($scope.crear_oferta_form1)
                if(crear_oferta_form1.$valid){
                    $scope.formActual = $scope.tabs[indice];
                    $scope.actualtab = indice;
                    aux = true;
                }else{
                    aux=false;
                }
                break;
            /*case 1:
                if(crear_oferta_form2.$valid && aux){
                    $scope.formActual = $scope.tabs[indice];
                    $scope.actualtab = indice;
                    aux2=true;
                }else{
                    aux2=false;
                }
                break;
            case 2:
                if(crear_oferta_form3.$valid && aux2){
                    $scope.formActual = $scope.tabs[indice];
                    $scope.actualtab = indice;
                    aux3=true;
                }else{
                    aux3=true;
                }
                break;
            case 3:
                if(crear_oferta_form4.$valid && aux3){
                    $scope.formActual = $scope.tabs[indice];
                    $scope.actualtab = indice;
                }
                break;
        }

    };*/

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

    
    var aux;
    aux = $scope.tiempo_disponible + " " + $scope.tiempo_tipo;
    console.log('aux'+aux);
    $scope.guardar = function(){
        console.log('aux'+aux);
        $scope.oferta.tiempo_para_estar_disponible = aux;
        $scope.oferta.$save(function(response){
            console.log('Se ha creado con exito la Oferta');
            $scope.textType="alert-success";
            $scope.oferta = "";
            $scope.oferta = new Oferta();
            $scope.tiempo_tipo="";
            $scope.tiempo_disponible=1;
            $scope.info_crear_oferta = "Oferta creada exitosamente";
            $scope.hide=false;
            $scope.actualtab = 0;
            $scope.formActual = $scope.tabs[0];


            /*
            $window.location.href = '/administrarOferta/';
            

            appoferta.controller('mensajeExitoCrearOferta',['$scope',function($scope){
                $scope.hide2=false;
                $scope.info_crear_oferta_success = "Oferta creada exitosamente";
            }]);*/
            
        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.textType="alert-danger";
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


appoferta.controller('OfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    $http.get(urls.BASE_API+'/ofertas',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.listaOfertas = response.results;
        console.log($scope.listaOfertas);
    }).error(function(){
        console.log('hubo un error');
    });
}]);









