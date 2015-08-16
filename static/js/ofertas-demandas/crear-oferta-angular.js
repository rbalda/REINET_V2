
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
    return $resource("/api/ofertas/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);


function getQueryVariable(variable, url) {
    var query = url;
    var vars = query.split("?");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    } 
    return "";
}

appoferta.controller('OfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    $http.get(urls.BASE_API+'/ofertas/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.pagina = 1;
        $scope.listaOfertas = response.results;
        $scope.contador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.siguiente = urls.BASE_API+'/ofertas/?page=1';
        }else{
            $scope.siguiente=response.next;
        }
        if(response.previous == null){
            $scope.anterior = urls.BASE_API+'/ofertas/?page=' + $scope.contador;
        }else{
            $scope.anterior=response.next;
        }
    }).error(function(){
        console.log('hubo un error');
    });
    $scope.irAlsiguiente = function(){
        $http.get($scope.siguiente,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.pagina = getQueryVariable('page', $scope.siguiente);
            $scope.listaOfertas = response.results;
            $scope.contador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.siguiente = urls.BASE_API+'/ofertas/?page=1';
            }else{
                $scope.siguiente=response.next;
            }
            if(response.previous == null){
                $scope.anterior = urls.BASE_API+'/ofertas/?page=' + $scope.contador;
            }else{
                $scope.anterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.irAlanterior = function(){
        $http.get($scope.anterior,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.pagina = getQueryVariable('page', $scope.anterior);
            $scope.listaOfertas = response.results;
            $scope.contador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.siguiente = urls.BASE_API+'/ofertas/?page=1';
            }else{
                $scope.siguiente=response.next;
            }
            if(response.previous == null){
                $scope.anterior = urls.BASE_API+'/ofertas/?page=' + $scope.contador;
            }else{
                $scope.anterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
}]);


appoferta.controller('MisOfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas!");
    $http.get(urls.BASE_API+'/misOfertas/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.MOpagina = 1;
        $scope.MOlistaOfertas = response.results;
        $scope.MOcontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.MOsiguiente = urls.BASE_API+'/ofertas/?page=1';
        }else{
            $scope.MOsiguiente=response.next;
        }
        if(response.previous == null){
            $scope.MOanterior = urls.BASE_API+'/ofertas/?page=' + $scope.MOcontador;
        }else{
            $scope.MOanterior=response.next;
        }
        console.log($scope.MOlistaOfertas);
        console.log($scope.MOsiguiente);
        console.log($scope.MOanterior);
    }).error(function(){
        console.log('hubo un error');
    });
    $scope.irAlsiguientePublicada = function(){
        $http.get($scope.MOsiguiente,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.MOpagina = getQueryVariable('page', $scope.siguiente);
            $scope.MOlistaOfertas = response.results;
            $scope.MOcontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.MOsiguiente = urls.BASE_API+'/ofertas/?page=1';
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/ofertas/?page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.previous;
            }
            console.log($scope.MOlistaOfertas);
            console.log($scope.MOsiguiente);
            console.log($scope.MOanterior);
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.irAlanteriorPublicada = function(){
        $http.get($scope.MOanterior,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.MOpagina = getQueryVariable('page', $scope.anterior);
            $scope.MOlistaOfertas = response.results;
            $scope.MOcontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.MOsiguiente = urls.BASE_API+'/ofertas/?page=1';
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/ofertas/?page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.previous;
            }
            console.log($scope.MOlistaOfertas);
            console.log($scope.MOsiguiente);
            console.log($scope.MOanterior);
        }).error(function(){
            console.log('hubo un error');
        });
    };
}]);









