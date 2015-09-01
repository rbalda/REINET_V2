
var appdemanda = angular.module('redInn');

appdemanda.config(['flowFactoryProvider', function (flowFactoryProvider) {

}]);

appdemanda.controller('crearDemandaFormController',['$scope','$rootScope','Demanda','$timeout','$window','$cookies','$compile','Demanda',function($scope,$rootScope,Demanda,$timeout,$window,$cookies,$compile,flowFactoryProvider){
    // dentro del scope van modelos

    $scope.setHead = function (file, chunk, isTest) {
            return {
                'X-CSRFToken': $cookies["csrftoken"]
            };      
    };

    $scope.demanda = new Demanda();
    $scope.copia_demanda = $window.demanda_copia;
    $scope.copia_tags = $window.tags_copia;

    $scope.items_date = [{tipo: "A\u00F1o/s", valor: 0 },{tipo: "Mes/es", valor: 1 }];

    $scope.demanda_id = 0;
    $scope.hide = true;
    $scope.validar_form=true;
    $scope.forms = {};
    $scope.imagen = {};
    $scope.txt_imagen_lst = [];
    $scope.indexImagen = 0;

    var tiempo='1';
    var duracion='A\u00F1o/s';

    if($scope.copia_demanda){
        tiempo = $window.demanda_tiempo;
        duracion = $window.demanda_duracion;

        if(duracion===1){
            $scope.tiempo_tipo = 'A\u00F1o/s';
        }else{
            $scope.tiempo_tipo = 'Mes/es';
        }

        $scope.tiempo_disponible = tiempo; 

        $scope.demanda2 = {
            descripcion : $scope.copia_demanda.descripcion,
            dominio : $scope.copia_demanda.dominio,
            subdominio : $scope.copia_demanda.subdominio,
            perfil_beneficiario : $scope.copia_demanda.perfil_beneficiario,
            perfil_cliente : $scope.copia_demanda.perfil_cliente,
            alternativas_soluciones_existentes : $scope.copia_demanda.alternativas_soluciones_existentes,
            importancia_resolver_necesidad : $scope.copia_demanda.importancia_resolver_necesidad,
            lugar_donde_necesita : $scope.copia_demanda.lugar_donde_necesita
        };
        if($scope.demanda2!== undefined){
            $scope.demanda = new Demanda($scope.demanda2);    
        };
        var tags=[];
        if($scope.copia_tags){
            for ( t in $scope.copia_tags){
                tags.push({ text: $scope.copia_tags[t] });
            };
            $scope.demanda.tags=tags;
        };

    }else{
        console.log('copia demanda no existe');
    };


    function isEmpty(myObject) {
        for(var key in myObject) {
            if (myObject.hasOwnProperty(key)) {
                return false;
            };
        };

        return true;
    };

    var tags={};
    $scope.$watch('demanda.tags',function(palabra){
        console.log('dentro de watch palabras_clave');
        console.log(palabra);
        tags = palabra;

        if(!isEmpty(tags)){
            console.log('tags'+tags);
            console.log(tags);
            $scope.demanda.tags = tags;
        }
    });


    $scope.$watch('txt_imagen_lst', function (value) {

    }, true);

    $scope.exitoSubida = function (file) {
        file.cancel();
        if($scope.txt_imagen_lst.length !== 0){
            $scope.txt_imagen_lst = $scope.txt_imagen_lst.slice(1,$scope.txt_imagen_lst.length-1);
        };
    };

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
            };
        };
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
        };
    };

    $scope.tiempoDisponibleInput = function(val){
        if(val===undefined){
            console.log('no tiempoDisponibleInput val');
        }else{
            console.log(val);
            tiempo=val;
        };
    };
    

    function loadImagen(id){
        console.log('dentro de loadImagen');
        $scope.imagen.flow.opts.query = {'id_demanda': id , 'descripcion':JSON.stringify(crearJSON($scope.imagen.flow.files))};
        console.log($scope.imagen.flow.opts.query['descripcion'])
        console.log( typeof $scope.imagen.flow.opts.query['descripcion'])
        $scope.imagen.flow.upload(); 
    };

    $scope.removerImagen = function(item,index){
        if(item!==undefined){
            item.cancel();
            if($scope.txt_imagen_lst.length !== 0){
                $scope.txt_imagen_lst = $scope.txt_imagen_lst.slice(1,$scope.txt_imagen_lst.length-1);
            };  
        };
    };


    function crearJSON(list){
        var json_array = [];
        var i=0;
        var value;
        for (l in list){
            value = String(list[l].uniqueIdentifier);
            json_array.push({value:value,descripcion:$scope.txt_imagen_lst[i]});
            i++;
        };
        return json_array;
    }


    $scope.guardar = function(){

        $scope.demanda.tiempo_para_estar_disponible=tiempo + " " + duracion;

        $scope.demanda.$save(function(response){
            console.log('Se ha creado con exito la demanda');

            $scope.demanda_id = $scope.demanda.id_demanda;
            loadImagen($scope.demanda.id_demanda);

            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.demanda = new Demanda();
            $scope.tiempo_tipo="";
            $scope.tiempo_disponible=1;
            $scope.info_crear_demanda = "Demanda creada exitosamente";
            $scope.hide=false;          
        },
        function(response){
            console.log('Ha ocurrido un error');
            $scope.textType="alert-danger";
            $scope.iconoClass="glyphicon-exclamation-sign";
            $scope.info_crear_demanda = "Hubo un error al crear demanda";
            $scope.hide=false;

        });
    }



//fin de controller
}]);


appdemanda.factory('Demanda',['$resource',function($resource){
    return $resource("/api/demandas/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);


appdemanda.controller('CargarDemandasSelectController',['$scope','$http','urls',function($scope,$http,urls){
    $http.get(urls.BASE_API+'/misDemandasAll/',{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.listaDemandas = response.results;
    }).error(function(){
        console.log('hubo un error en select demandas');
    });

    $scope.selectDemandas = function(item){
        console.log(item);
    }
    
}]);




//INICIO DEMANDAS

function getQueryVariable(variable, url) {
    var query = url;
    var vars = query.split("page=");
    console.log(query);
    if (vars[1]!=null){
        return vars[1];
    }
    return "1";
}

//CONTROLADOR LISTA OFERTAS DE LA RED
appdemanda.controller('OfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    $http.get(urls.BASE_API+'/ofertas/' + "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
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
                $scope.siguiente = urls.BASE_API+'/ofertas/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.siguiente=response.next;
            }
            if(response.previous == null){
                $scope.anterior = urls.BASE_API+'/ofertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.contador;
            }else{
                $scope.anterior=response.previous;
            }
            console.log('buscando: ' + $scope.busqueda_ofertas);
            console.log($scope.siguiente);
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
                $scope.siguiente = urls.BASE_API+'/ofertas/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.siguiente=response.next;
            }
            if(response.previous == null){
                $scope.anterior = urls.BASE_API+'/ofertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.contador;
            }else{
                $scope.anterior=response.previous;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.$on('buscando', function(){
        $http.get(urls.BASE_API+'/ofertas/' + "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.pagina = 1;
            $scope.listaOfertas = response.results;
            $scope.contador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.siguiente = urls.BASE_API+'/ofertas/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.siguiente=response.next;
            }
            if(response.previous == null){
                $scope.anterior = urls.BASE_API+'/ofertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.contador;
            }else{
                $scope.anterior=response.next;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    });
}]);

//CONTROLADOR LISTA OFERTAS PUBLICADAS
appdemanda.controller('MisOfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas!");
    $http.get(urls.BASE_API+'/misOfertas/' + "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.MOpagina = 1;
        $scope.MOlistaOfertas = response.results;
        $scope.MOcontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas;
        }else{
            $scope.MOsiguiente=response.next;
        }
        if(response.previous == null){
            $scope.MOanterior = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.MOcontador;
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
                $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.next;
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
                $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.next;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.$on('buscando', function(){
        $http.get(urls.BASE_API+'/misOfertas/' + "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.MOpagina = 1;
            $scope.MOlistaOfertas = response.results;
            $scope.MOcontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.MOsiguiente = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.MOsiguiente=response.next;
            }
            if(response.previous == null){
                $scope.MOanterior = urls.BASE_API+'/misOfertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.MOcontador;
            }else{
                $scope.MOanterior=response.next;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    });
}]);

//CONTROLADOR LISTA OFERTAS BORRADOR
appdemanda.controller('MisOfertasBorradoresControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas Borradores!");
    $http.get(urls.BASE_API+'/misOfertasBorradores/' + "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.Borradorespagina = 1;
        $scope.BorradoreslistaOfertas = response.results;
        $scope.Borradorescontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas;
        }else{
            $scope.Borradoressiguiente=response.next;
        }
        if(response.previous == null){
            $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.Borradorescontador;
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
                $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.Borradoressiguiente=response.next;
            }
            if(response.previous == null){
                $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.Borradorescontador;
            }else{
                $scope.Borradoresanterior=response.next;
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
                $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.Borradoressiguiente=response.next;
            }
            if(response.previous == null){
                $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.Borradorescontador;
            }else{
                $scope.Borradoresanterior=response.next;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    };
    $scope.$on('buscando', function(){
        $http.get(urls.BASE_API+'/misOfertasBorradores/' + "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.Borradorespagina = 1;
            $scope.BorradoreslistaOfertas = response.results;
            $scope.Borradorescontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.Borradoressiguiente = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.Borradoressiguiente=response.next;
            }
            if(response.previous == null){
                $scope.Borradoresanterior = urls.BASE_API+'/misOfertasBorradores/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.Borradorescontador;
            }else{
                $scope.Borradoresanterior=response.next;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    });
}]);


appdemanda.controller('busquedaControlador',['$rootScope', '$scope','$http','urls',function($rootScope, $scope,$http,urls){
    $scope.buscarOfertas = function(){
        $rootScope.$broadcast('buscando');
    }
}]);

appdemanda.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});