'use strict';

angular.module('medizam')
  .controller('ResultsCtrl', [ '$scope', function ($scope) {
        $scope.results = [
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 80
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 72
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 64
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 49
            },
            {
                name: "Zoloft 50mg",
                image: "images/mocks/5B_3quart_low.jpg",
                accuracy: 39
            }
        ];
  }]);
