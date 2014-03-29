'use strict';

angular.module('medizam')
  .controller('PhotoCtrl', [ '$scope', '$resource', function ($scope, $resource) {
        var Files = $resource('/api/upload/:id', { id: "@id" });

        angular.extend($scope, {
            model: { file: null },

            upload: function(model) {
                Files.prototype.$save.call(model.file, function(self, headers) {
                    // Handle server response
                });
            }
        });

        $scope.takePicture = function() {
            angular.element('#picture-input').click();

        };
  }]);
