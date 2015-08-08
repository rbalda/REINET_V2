
var appoferta = angular.module('redInn');

appoferta.controller('crearOfertaFormController',['$scope' ,function($scope,oferta){
    // dentro del scope van modelos
    console.log('dentro del crearOfertaAngular');

    $scope.oferta = oferta;

    $scope.tabs = ['/static/templates-ofertas-demandas/crear_oferta_form1.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form2.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form3.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form4.html',
                    '/static/templates-ofertas-demandas/crear_oferta_form5.html'];

    $scope.actualtab = 0;
    $scope.formActual = $scope.tabs[$scope.actualtab];

    $scope.items_tipo = [{tipo: 'Emprendimiento', valor: 0 },{tipo: 'Tecnolog\u00EDa', valor: 1 },{tipo: 'Prototipo', valor: 2 }];
    $scope.items_date = [{tipo: 'A\u00F1o', valor: 0 },{tipo: 'Mes', valor: 1 },{tipo: 'D\u00EDa', valor: 2 }];

    $scope.oferta={
        tipo_oferta : $scope.items_tipo[0],
        tiempo_oferta : $scope.items_date[0]
        }


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

    //$scope.oferta = new oferta();



    $scope.guardar = function(){
        $scope.oferta.$create();
    }

//fin de controller
}]);

appoferta.factory('oferta',['$resource',function($resource){

    var oferta ={

        create:function(url,obj,errors){
            return $http.post(url,obj)
            success(function(response,status,headers,config){
                angular.extend(obj,response);
            });

        }
    }

    return $resource("http://localhost:8000/api/Ofertas/:id/",{id:'@id'},{
        update:{
            method:'PUT'
        }
    })
}]);














/*
    $scope.oferta={
        nombre:'',
        descripcion:'',
        dominio:'',
        subdominio:'',
        cliente_perfil:'',
        beneficiario_perfil:'',
        tendencias_relevantes:'',
        alternativas_existentes:'',
        tiempo_disponibilidad:'',
        tiempo_disponibilidad_tipo:'',
        estrategia_crecimiento:'',
        propiedad_intelectual:'',
        evidencia_traccion:''

    }

    $scope.canvas={
        socio_clave:'',
        activiades_clave:'',
        recursos_clave:'',
        propuesta_valor:'',
        relaciones_clientes:'',
        canales_distribucion:'',
        segmentos_mercado:'',
        estructura_costos:'',
        fuente_ingresos:''
    }

    $scope.diagramapoter={
        competidores:'',
        consumidores:'',
        sustitutos:'',
        proveedores:'',
        nuevos_entrantes:''
    }
    */