'use strict';

angular.module('medizam')
  .controller('ResultsCtrl', [ '$scope', function ($scope) {
        $scope.results = [
            {
                name: "Doliprane 500mg",
                image: "images/mocks/5B_3quart_low.jpg"
            },
            {
                name: "Doliprane 500mg",
                image: "images/mocks/5B_3quart_low.jpg"
            },
            {
                name: "Doliprane 500mg",
                image: "images/mocks/5B_3quart_low.jpg"
            },
            {
                name: "Doliprane 500mg",
                image: "images/mocks/5B_3quart_low.jpg"
            },
            {
                name: "Doliprane 500mg",
                image: "images/mocks/5B_3quart_low.jpg"
            }
        ];
  }]);
