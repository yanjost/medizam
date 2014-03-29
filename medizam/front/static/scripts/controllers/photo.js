'use strict';

angular.module('medizam')
  .controller('PhotoCtrl', [ '$scope', '$resource', function ($scope, $resource) {
        var Files = $resource('/api/upload');

        angular.extend($scope, {
            model: { file: null },

            upload: function(model) {
                Files.prototype.$save.call(model.file, function(response) {
                    $scope.previewImage = response.preview;
                });
            }
        });

        $scope.takePicture = function() {
            angular.element('#picture-input').click();

        };
  }]);
