'use strict';

angular.module('medizam')
  .controller('ResultDetailsCtrl', [ '$scope', '$routeParams', '$sce', 'ResultsService', function ($scope, $routeParams, $sce, resultsService) {
        angular.forEach(resultsService.getLastResults(), function(result) {
            if (result.id === $routeParams.id)
                $scope.result = result;
        });

        if (typeof $scope.result.vidal_url === 'string')
            $scope.result.vidal_url = $sce.trustAsResourceUrl($scope.result.vidal_url);
  }]);
