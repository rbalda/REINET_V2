var redInn = angular.module('redInn',['ngResource','ngAnimate','ngRoute','ngCookies']);

redInn.config(['$routeProvider',function($routeProvider){
    $routeProvider.
    when('/incubaciones',{
        templateUrl:'static/partials/incubacion_institucion.html'}).
    when('/incubaciones/:id',{
        templateUrl:'static/partials/incubacion1_institucion.html',
        controller:'incubaController'}).
    when('/crear',{
        templateUrl:'static/partials/crear_incubacion.html'})
    .otherwise({
        templateUrl:'static/partials/incubacion_institucion.html'});



}]);

redInn.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


redInn.controller('mainController',['$scope','$location',function($scope,$location){
    $scope.go = function(url){
        $location.path(url);
    };
}]);

redInn.controller('createController',['$scope',function($scope){
    $scope.alcance='institucion';
}]);

redInn.controller('incubaController',['$scope','Incubacion','$routeParams','Incubada','$filter',function($scope,Incubacion,$routeParams,Incubada,$filter){
    $scope.modal_content=null;
    $scope.modal_possible=[
        {
            'title':'Crear Convocatoria',
            'tpl':'static/partials/crear_convocatoria.html'
        },
        {
            'title':'Invitar Consultor',
            'tpl':'static/partials/invitar_consultor.html'
        },
        {
            'title':'Crear Milestone',
            'tpl':'static/partials/crear_milestone.html'
        },
        {
            'title':'Aumentar Alcance',
            'tpl':'static/partials/aumentar_alcance.html'
        },
        {
            'title':'Terminar Incubacion',
            'tpl':'static/partials/terminar_incubacion.html'
        },
        {
            'title':'Suspender Incubacion',
            'tpl':'static/partials/suspender_incubacion.html'
        }
    ];
    $scope.incubacion = Incubacion.get({id:$routeParams.id});
    $scope.incubadas = Incubada.query();


    $scope.setModal = function(n){
        $scope.modal_content=$scope.modal_possible[n];
    };

}]);

redInn.controller('IncubacionController',['$scope','Incubacion','$cookieStore',function($scope,Incubacion,$cookieStore){
    this.incubaciones = Incubacion.query();
    this.temp=0;

    this.isToday = function(fecha){
        return Date(fecha) == Date.now();
    }
}]);


redInn.factory('Incubacion',['$resource',function($resource){
    return $resource('../list-incubaciones/:id',{},{
        update:{
            method:'PUT'
        }
    });
}]);

redInn.factory('Incubada',['$resource',function($resource){
    return $resource('../list-incubadas/:id',{},{
        update:{
            method:'PUT'
        }
    });
}]);


redInn.controller('crearIncubacionController',['$scope','Incubacion','$cookieStore',function($scope,Incubacion,$cookieStore) {
    $scope.incubacion = new Incubacion();
    var a =$cookieStore.get('id_autor');
    $scope.addIncubacion= function() {
        $scope.autor=a;
        console.log(a);
        $scope.incubacion.$save();
    }
}]);