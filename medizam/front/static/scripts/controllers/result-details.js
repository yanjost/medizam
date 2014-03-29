'use strict';

angular.module('medizam')
  .controller('ResultDetailsCtrl', [ '$scope', '$routeParams', function ($scope, $routeParams) {
        $scope.resultId = $routeParams.id;
  }]);
