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
                controller: 'MainCtrl'
            })
            .when('/photo', {
                templateUrl: 'views/photo.html',
                controller: 'PhotoCtrl'
            })
            .when('/results', {
                templateUrl: 'views/results.html',
                controller: 'ResultsCtrl'
            })
            .when('/result-details', {
                templateUrl: 'views/result-details.html',
                controller: 'ResultDetailsCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });
