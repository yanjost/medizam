'use strict';

angular
    .module('medizam', [
        'ngResource',
        'ngSanitize',
        'ngRoute',
        'mobile-angular-ui',
        'ur.file'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl',
                title: 'MediZam!'
            })
            .when('/photo', {
                templateUrl: 'views/photo.html',
                controller: 'PhotoCtrl',
                title: 'Automatic',
                backActionLink: '#/',
                backActionName: 'Home'
            })
            .when('/results', {
                templateUrl: 'views/results.html',
                controller: 'ResultsCtrl',
                title: 'Results',
                backActionLink: '#/',
                backActionName: 'Home'
            })
            .when('/results/:id/details', {
                templateUrl: 'views/result-details.html',
                controller: 'ResultDetailsCtrl',
                title: 'Result details',
                backActionLink: '#/results',
                backActionName: 'Results'
            })
            .otherwise({
                redirectTo: '/'
            });
    }).run([ '$rootScope', '$route', function($rootScope, $route) {
        $rootScope.$on('$routeChangeSuccess', function(event, route) {
            $rootScope.viewTitle = route.$$route.title;
            $rootScope.hasBackAction = route.$$route.backActionLink && route.$$route.backActionName;
            $rootScope.backActionLink = route.$$route.backActionLink;
            $rootScope.backActionName = route.$$route.backActionName;
        });
    }]);
