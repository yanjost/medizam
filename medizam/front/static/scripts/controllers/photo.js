'use strict';

angular.module('medizam')
  .controller('PhotoCtrl', [ '$scope', '$resource', '$location', 'ResultsService', function ($scope, $resource, $location, resultsService) {
        var Files = $resource('/api/upload');

        $scope.inProgress = false;

        angular.extend($scope, {
            model: { file: null },

            upload: function(model) {
                $scope.inProgress = true;
                resultsService.clearLastResults();

                Files.prototype.$save.call(model.file, function(response) {
                    resultsService.setLastResults(response.results);
                    $scope.inProgress = false;
                    $location.path('/results');
                });
            }
        });

        $scope.takePicture = function() {
            angular.element('#picture-input').click();

        };
  }]);
