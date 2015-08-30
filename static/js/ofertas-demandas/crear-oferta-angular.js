
var appoferta = angular.module('redInn');

appoferta.config(['flowFactoryProvider', function (flowFactoryProvider) {
    /*flowFactoryProvider.defaults = {
        headers: function (file, chunk, isTest) {
                    return {
                        'X-CSRFToken': $cookies.get("csrftoken")
                    }
                }
        //target : '',
        //testChunks:false,
        //permanentErrors: [500, 501],
        //maxChunkRetries: 1,
        //chunkRetryInterval: 5000,
        //simultaneousUploads: 4
    };

    flowFactoryProvider.on('fileAdded',function(file,event,flow){
        console.log('dentro de fileAdded');

    });

    flowFactoryProvider.on('filesSubmitted',function(file,event,flow){
        console.log('dentro de filesSubmitted');
    });*/

}]);

appoferta.controller('crearOfertaFormController',['$scope','$rootScope','Oferta','$timeout','$window','$cookies','$compile',function($scope,$rootScope,Oferta,$timeout,$window,$cookies,$compile,flowFactoryProvider){
    // dentro del scope van modelos

    $scope.setHead = function (file, chunk, isTest) {
            return {
                'X-CSRFToken': $cookies["csrftoken"]
            };      
    };

    console.log('dentro del crearOfertaAngular');

    $scope.oferta = new Oferta();
    $scope.copia_oferta = $window.oferta_copia;
    $scope.copia_tags = $window.tags_copia;

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_date = [{tipo: "A\u00F1o", valor: 0 },{tipo: "Mes", valor: 1 }];

    $scope.oferta_id = 0;
    $scope.tipo = 0;
    $scope.hide = true;
    $scope.validar_form=true;
    $scope.forms = {};
    $scope.imagen = {};
    $scope.txt_imagen_lst = [];
    $scope.indexImagen = 0;

    var tiempo='1';
    var duracion='A\u00F1o';

    if($scope.copia_oferta){
        var tipo = parseInt($scope.copia_oferta.tipo);
        tiempo = $window.oferta_tiempo;
        duracion = $window.oferta_duracion;

        if(duracion===1){
            $scope.tiempo_tipo = 'A\u00F1o';
        }else{
            $scope.tiempo_tipo = 'Mes';
        }

        $scope.tiempo_disponible = tiempo; 

        $scope.oferta2 = {
            tipo : tipo,
            descripcion : $scope.copia_oferta.descripcion,
            dominio : $scope.copia_oferta.dominio,
            subdominio : $scope.copia_oferta.subdominio,
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
        var tags=[];
        if($scope.copia_tags){
            for ( t in $scope.copia_tags){
                tags.push({ text: $scope.copia_tags[t] });
            }
            $scope.oferta.tags=tags;
        }

    }else{
        console.log('copia oferta no existe');
    }


    function isEmpty(myObject) {
        for(var key in myObject) {
            if (myObject.hasOwnProperty(key)) {
                return false;
            };
        };

        return true;
    };

    var tags={};
    $scope.$watch('oferta.tags',function(palabra){
        console.log('dentro de watch palabras_clave');
        console.log(palabra);
        tags = palabra;

        if(!isEmpty(tags)){
            console.log('tags'+tags);
            console.log(tags);
            $scope.oferta.tags = tags;
        };
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
        $scope.imagen.flow.opts.query = {'id_oferta': id , 'descripcion':JSON.stringify(crearJSON($scope.imagen.flow.files))};
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

        $scope.oferta.tiempo_para_estar_disponible=tiempo + " " + duracion;

        $scope.oferta.$save(function(response){
            console.log('Se ha creado con exito la Oferta');

            $scope.oferta_id = $scope.oferta.id_oferta;
            loadImagen($scope.oferta.id_oferta);

            $scope.textType="alert-success";
            $scope.iconoClass="glyphicon-ok-sign";
            $scope.oferta = new Oferta();
            $scope.tiempo_tipo="";
            $scope.tiempo_disponible=1;
            $scope.info_crear_oferta = "Oferta creada exitosamente";
            $scope.hide=false;          
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

//CONTROLADOR LISTA OFERTAS DE LA RED
appoferta.controller('OfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
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
appoferta.controller('MisOfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
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
appoferta.controller('MisOfertasBorradoresControlador',['$scope','$http','urls',function($scope,$http,urls){
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

//CONTROLADOR LISTA OFERTAS EN LAS QUE PARTICIPO
appoferta.controller('MiembroOfertasControlador',['$scope','$http','urls',function($scope,$http,urls){
    console.log("Mis Ofertas Borradores!");
    $http.get(urls.BASE_API+'/miembroOfertas/'+ "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
    .success(function(response){
        $scope.miembropagina = 1;
        $scope.miembrolistaOfertas = response.results;
        $scope.miembrocontador = Math.ceil(response.count/5);
        if(response.next == null){
            $scope.miembrosiguiente = urls.BASE_API+'/miembroOfertas//?busqueda=' + $scope.busqueda_ofertas;
        }else{
            $scope.miembrosiguiente=response.next;
        }
        if(response.previous == null){
            $scope.miembroanterior = urls.BASE_API+'/miembroOfertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.miembrocontador;
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
    $scope.$on('buscando', function(){
        $http.get(urls.BASE_API+'/miembroOfertas/'+ "?busqueda=" + $scope.busqueda_ofertas,{},{headers:{"Content-Type":"application/json"}})
        .success(function(response){
            $scope.miembropagina = 1;
            $scope.miembrolistaOfertas = response.results;
            $scope.miembrocontador = Math.ceil(response.count/5);
            if(response.next == null){
                $scope.miembrosiguiente = urls.BASE_API+'/miembroOfertas//?busqueda=' + $scope.busqueda_ofertas;
            }else{
                $scope.miembrosiguiente=response.next;
            }
            if(response.previous == null){
                $scope.miembroanterior = urls.BASE_API+'/miembroOfertas/?busqueda=' + $scope.busqueda_ofertas + '&page=' + $scope.miembrocontador;
            }else{
                $scope.miembroanterior=response.next;
            }
        }).error(function(){
            console.log('hubo un error');
        });
    });
}]);

appoferta.controller('busquedaControlador',['$rootScope', '$scope','$http','urls',function($rootScope, $scope,$http,urls){
    $scope.buscarOfertas = function(){
        $rootScope.$broadcast('buscando');
    }
}]);

appoferta.controller('editar_oferta_form', ['$scope','$window', 'Oferta', function( $scope, $window, Oferta){

    $scope.editar_oferta=$window.oferta_editar;

    $scope.oferta = new Oferta(); 

    $scope.items_tipo = [{tipo: "Emprendimiento", valor: 0 },{tipo: "Tecnolog\u00EDa", valor: 1 },{tipo: "Prototipo", valor: 2 }];
    $scope.items_date = [{tipo: "A\u00F1o", valor: 0 },{tipo: "Mes", valor: 1 }];

    $scope.tipo = 0;
    $scope.hide = true;

    if($scope.editar_oferta !== undefined){
        $scope.editar_oferta2 = {
            //tipo : $scope.copia_oferta.tipo,
            nombre : $scope.editar_oferta.nombre,
            descripcion : $scope.editar_oferta.descripcion,
            dominio : $scope.editar_oferta.dominio,
            subdominio : $scope.editar_oferta.subdominio,
            perfil_beneficiario : $scope.editar_oferta.perfil_beneficiario,
            perfil_cliente : $scope.editar_oferta.perfil_cliente,
            descripcion_soluciones_existentes : $scope.editar_oferta.descripcion_soluciones_existentes,
            estado_propieada_intelectual : $scope.editar_oferta.estado_propieada_intelectual,
            evidencia_traccion : $scope.editar_oferta.evidencia_traccion,
            cuadro_tendencias_relevantes : $scope.editar_oferta.cuadro_tendencias_relevantes,

            fk_diagrama_competidores : {
                competidores : $scope.editar_oferta.poter_competidores,
                sustitutos : $scope.editar_oferta.poter_sustitutos,
                consumidores : $scope.editar_oferta.poter_consumidores,
                proveedores : $scope.editar_oferta.poter_proveedores,
                nuevosMiembros : $scope.editar_oferta.poter_nuevosMiembros
            },

            fk_diagrama_canvas : {
                asociaciones_clave : $scope.editar_oferta.canvas_asociaciones_clave,
                actividades_clave : $scope.editar_oferta.canvas_actividades_clave,
                recursos_clave : $scope.editar_oferta.canvas_recursos_clave,
                propuesta_valor : $scope.editar_oferta.canvas_propuesta_valor,
                relacion_clientes : $scope.editar_oferta.canvas_relacion_clientes,
                canales_distribucion : $scope.editar_oferta.canvas_canales_distribucion,
                segmento_mercado : $scope.editar_oferta.canvas_segmento_mercado,
                estructura_costos : $scope.editar_oferta.canvas_estructura_costos,
                fuente_ingresos : $scope.editar_oferta.canvas_fuente_ingresos
            }
        };
        if($scope.editar_oferta2!== undefined){
            $scope.oferta = new Oferta($scope.editar_oferta2);    
        }

    }else{
        console.log('copia oferta no existe');
    }
    


}]);

appoferta.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});









