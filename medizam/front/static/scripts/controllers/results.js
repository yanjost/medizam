'use strict';

angular.module('medizam')
  .controller('ResultsCtrl', [ '$scope', 'ResultsService', function ($scope, resultsService) {
        $scope.results = resultsService.getLastResults();
  }]);
