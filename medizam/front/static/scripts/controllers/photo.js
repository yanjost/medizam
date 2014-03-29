'use strict';

angular.module('medizam')
  .controller('PhotoCtrl', [ '$scope', '$resource', 'ResultsService', function ($scope, $resource, resultsService) {
        var Files = $resource('/api/upload');

        $scope.inProgress = false;

        angular.extend($scope, {
            model: { file: null },

            upload: function(model) {
                $scope.inProgress = true;
                resultsService.clearLastResults();

                Files.prototype.$save.call(model.file, function(response) {
                    $scope.inProgress = false;
                    resultsService.setLastResults(response.results);
                });
            }
        });

        $scope.takePicture = function() {
            angular.element('#picture-input').click();

        };
  }]);
