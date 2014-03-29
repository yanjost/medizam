'use strict';

angular.module('medizam')
  .controller('ResultsCtrl', [ '$scope', function ($scope) {
        $scope.results = [
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 80,
                id: 1
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 72,
                id: 2
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 64,
                id: 3
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 49,
                id: 4
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 39,
                id: 5
            }
        ];
  }]);
