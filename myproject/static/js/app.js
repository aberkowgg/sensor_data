/**
 * Accepts a wrapper and optional parameters associative array.
 * The wrapper is the div the contains the dynamically loaded html you wish to initialize angular for.
 * Parameteres are dynamic and options
 *
 * @param wrapper
 * @param params - array
 */
function initAngular(wrapper, view){
    angular.element($('body')).injector().invoke(function($compile){
        var obj=wrapper;
        var scope=obj.scope();
        // generate dynamic content
        if(view){
            obj.html(view);
        }
        // compile!!!
        $compile(obj.contents())(scope);
    });
}


//Define module, associate angular app with part of html document.
var app = angular.module('app', []);


//Configure the html template to recognize {[ ]} instead of {{ }} for angular scope variables to avoid conflict with jinja.
app.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[').endSymbol(']}');
});

//init appCtrl
app.controller('appCtrl', appCtrl);


function appCtrl($scope, $http, $timeout, $q) {
  var vm = this;
  vm.ordered_key = ['message_count', 'motion', 'light_data', 'humidity', 'temperature', 'pressure']

  vm.get_sensor_data = function () {
      vm.loading_sensor_error = false;
      vm.loading_sensor_data = true;

      return $http({
          method  : 'GET',
          url     : '/refresh_sensor_data'
        }).success(function(data) {
          vm.sensor_data = data.response;
          vm.loading_sensor_data = false;
        }).error(function (data) {
          vm.loading_sensor_data = false;
          vm.loading_sensor_error = true;
        });
      }


  vm.meta_modal = function(data) {
    return $http({
      method  : 'POST',
      url     : '/meta_modal',
      data    : data
    }).success(function(data) {
      initAngular($('#modal_master_body'), data.view);
      $('#modal_master').modal('show');
    });
  }


  vm.format_label = function (uf_label) {
      return uf_label.replace(/_/g, " ");
  }


  vm.format_value = function (key, uf_val) {
      var value;
      switch (key){
          case 'msg_type':
              value = uf_val + ' Message';
              break;
          case 'motion':
              value = uf_val === 0 ? "No Motion (0)" : "Moation (1)";
              break;
          case 'light_data':
              value = uf_val + ' lux';
              break;
          case 'humidity':
              value = uf_val + ' % RH';
              break;
          case 'temperature':
              value = uf_val + ' C';
              break;
          case 'pressure':
              value = uf_val + ' Pa';
              break;
          case 'latitude':
              value = parseFloat(uf_val) > 0 ? 'N ' + uf_val : 'S ' + (parseFloat(uf_val)*-1);
              break;
          case 'longitude':
              value = parseFloat(uf_val) > 0 ? 'E ' + uf_val : 'W ' + (parseFloat(uf_val)*-1);
              break;
          case 'altitude':
              value = uf_val + 'm';
              break;
          case 'gw_rssi':
              value = uf_val + 'dBm';
              break;
          default:
              value = uf_val;
              break;
      }
      return value;
  }

}