
var appoferta = angular.module('redInn');

appoferta.controller('crearOfertaFormController',['$scope','$rootScope','Oferta','$timeout','$window',function($scope,$rootScope,Oferta,$timeout,$window){
    // dentro del scope van modelos


    console.log('dentro del crearOfertaAngular');

    $scope.oferta = new Oferta();
    $scope.copia_oferta = $window.oferta_copia;
    $scope.copia_tags = $window.tags_copia;
    console.log('copia oferta');
    console.log($scope.copia_oferta);

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

    if($scope.copia_oferta){
        console.log('copia oferta existe');
        $scope.oferta2 = {
            //tipo : $scope.copia_oferta.tipo,
            descripcion : $scope.copia_oferta.descripcion,
            dominio : $scope.copia_oferta.descripcion,
            subdominio : $scope.copia_oferta.descripcion,
            perfil_beneficiario : $scope.copia_oferta.perfil_beneficiario,
            perfil_cliente : $scope.copia_oferta.perfil_cliente,
            descripcion_soluciones_existentes : $scope.copia_oferta.descripcion_soluciones_existentes,
            estado_propieada_intelectual : $scope.copia_oferta.estado_propieada_intelectual,
            evidencia_traccion : $scope.copia_oferta.evidencia_traccion,
            cuadro_tendencias_relevantes : $scope.copia_oferta.cuadro_tendencias_relevantes,

            fk_diagrama_competidores : {
                competidores : $scope.copia_oferta.poter_competidores,
                sustitutos : $scope.copia_oferta.poter_sustitutos,
                consumidores : $scope.copia_oferta.poter_consumidores,
                proveedores : $scope.copia_oferta.poter_proveedores,
                nuevosMiembros : $scope.copia_oferta.poter_nuevosMiembros
            },

            fk_diagrama_canvas : {
                asociaciones_clave : $scope.copia_oferta.canvas_asociaciones_clave,
                actividades_clave : $scope.copia_oferta.canvas_actividades_clave,
                recursos_clave : $scope.copia_oferta.canvas_recursos_clave,
                propuesta_valor : $scope.copia_oferta.canvas_propuesta_valor,
                relacion_clientes : $scope.copia_oferta.canvas_relacion_clientes,
                canales_distribucion : $scope.copia_oferta.canvas_canales_distribucion,
                segmento_mercado : $scope.copia_oferta.canvas_segmento_mercado,
                estructura_costos : $scope.copia_oferta.canvas_estructura_costos,
                fuente_ingresos : $scope.copia_oferta.canvas_fuente_ingresos
            }
        };
        if($scope.oferta2!== undefined){
            $scope.oferta = new Oferta($scope.oferta2);    
        }
        //if($scope.copia_tags){
        //    $scope.oferta.tags=$scope.copia_tags;
        //}
    }else{
        console.log('copia oferta no existe');
    }


    function isEmpty(myObject) {
        for(var key in myObject) {
            if (myObject.hasOwnProperty(key)) {
                return false;
            }
        }

        return true;
    }
    var tags={};
    $scope.$watch('oferta.tags',function(palabra){
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
    };

    $scope.atras = function(){
        if($scope.actualtab>0)
            $scope.actualtab=$scope.actualtab-1;
            $scope.formActual = $scope.tabs[$scope.actualtab];
    };

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

//CONTROLADOR LISTA OFERTAS DE LA RED
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

//CONTROLADOR LISTA OFERTAS PUBLICADAS
appoferta.controller('MisOfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas!");
    $http.get(urls.BASE_API+'/misOfertas/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.MOpagina = 1;
        $scope.MOlistaOfertas = response.results;
        $scope.MOcontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?page=1';
        }else{
            $scope.MOsiguiente=response.next;
        }
        if(response.previous == null){
            $scope.MOanterior = urls.BASE_API+'/misOfertas/?page=' + $scope.MOcontador;
        }else{
            $scope.MOanterior=response.next;
        }
    }).error(function(){
        console.log('hubo un error');
    });
    $scope.irAlsiguientePublicada = function(){
        $http.get($scope.MOsiguiente,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.MOpagina = getQueryVariable('page', $scope.MOsiguiente);
            $scope.MOlistaOfertas = response.results;
            $scope.MOcontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?page=1';
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/misOfertas/?page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.irAlanteriorPublicada = function(){
        $http.get($scope.MOanterior,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.MOpagina = getQueryVariable('page', $scope.MOanterior);
            $scope.MOlistaOfertas = response.results;
            $scope.MOcontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?page=1';
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/misOfertas/?page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
}]);

//CONTROLADOR LISTA OFERTAS BORRADOR
appoferta.controller('MisOfertasBorradoresControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas Borradores!");
    $http.get(urls.BASE_API+'/misOfertasBorradores/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.Borradorespagina = 1;
        $scope.BorradoreslistaOfertas = response.results;
        $scope.Borradorescontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?page=1';
        }else{
            $scope.Borradoressiguiente=response.next;
        }
        if(response.previous == null){
            $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?page=' + $scope.Borradorescontador;
        }else{
            $scope.Borradoresanterior=response.next;
        }
    }).error(function(){
        console.log('hubo un error');
    });
    $scope.irAlsiguienteBorrador = function(){
        $http.get($scope.Borradoressiguiente,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.Borradorespagina = getQueryVariable('page', $scope.Borradoressiguiente);
            $scope.BorradoreslistaOfertas = response.results;
            $scope.Borradorescontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?page=1';
            }else{
                $scope.Borradoressiguiente=response.next;
            }
            if(response.previous == null){
                $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?page=' + $scope.Borradorescontador;
            }else{
                $scope.Borradoresanterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.irAlanteriorBorrador = function(){
        $http.get($scope.Borradoresanterior,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.Borradorespagina = getQueryVariable('page', $scope.Borradoresanterior);
            $scope.BorradoreslistaOfertas = response.results;
            $scope.Borradorescontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?page=1';
            }else{
                $scope.Borradoressiguiente=response.next;
            }
            if(response.previous == null){
                $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?page=' + $scope.Borradorescontador;
            }else{
                $scope.Borradoresanterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
}]);

//CONTROLADOR LISTA OFERTAS EN LAS QUE PARTICIPO
appoferta.controller('MiembroOfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas Borradores!");
    $http.get(urls.BASE_API+'/miembroOfertas/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.miembropagina = 1;
        $scope.miembrolistaOfertas = response.results;
        $scope.miembrocontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.miembrosiguiente = urls.BASE_API+'/miembroOfertas/?page=1';
        }else{
            $scope.miembrosiguiente=response.next;
        }
        if(response.previous == null){
            $scope.miembroanterior = urls.BASE_API+'/miembroOfertas/?page=' + $scope.miembrocontador;
        }else{
            $scope.miembroanterior=response.next;
        }
    }).error(function(){
        console.log('hubo un error');
    });
    $scope.irAlsiguienteMiembro = function(){
        $http.get($scope.miembrosiguiente,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.miembropagina = getQueryVariable('page', $scope.miembrosiguiente);
            $scope.miembrolistaOfertas = response.results;
            $scope.miembrocontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.miembrosiguiente = urls.BASE_API+'/miembroOfertas/?page=1';
            }else{
                $scope.miembrosiguiente=response.next;
            }
            if(response.previous == null){
                $scope.miembroanterior = urls.BASE_API+'/miembroOfertas/?page=' + $scope.miembrocontador;
            }else{
                $scope.miembroanterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.irAlanteriorMiembro = function(){
        $http.get($scope.miembroanterior,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.miembropagina = getQueryVariable('page', $scope.miembroanterior);
            $scope.miembrolistaOfertas = response.results;
            $scope.miembrocontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.miembrosiguiente = urls.BASE_API+'/miembroOfertas/?page=1';
            }else{
                $scope.miembrosiguiente=response.next;
            }
            if(response.previous == null){
                $scope.miembroanterior = urls.BASE_API+'/miembroOfertas/?page=' + $scope.miembrocontador;
            }else{
                $scope.miembroanterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
}]);








