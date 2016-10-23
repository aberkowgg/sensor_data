//Define module, associate angular app with part of html document.

var app = angular.module('app', []);

//Configure the html template to recognize {[ ]} instead of {{ }} for angular scope variables to avoid conflict with jinja.
app.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[').endSymbol(']}');
});

app.controller('appCtrl', appCtrl);
function appCtrl($scope, $http, $timeout, $q) {
  var vm = this;
  vm.ordered_key = ['message_count', 'message_type', 'latitude', 'longitude', 'altitude', 'gw_rssi', 'reserved', 'motion',
      'light_data', 'humidity', 'temperature', 'pressure']

  vm.get_sensor_data = function () {
      vm.loading_sensor_data = true;
      console.log("clicked");
      return $http({
      method  : 'GET',
      url     : '/refresh_sensor_data'
    }).success(function(data) {
      vm.sensor_data = data.response;
      vm.loading_sensor_data = false;
    });
  }

  vm.format_label = function (uf_label) {
      var label;
      if(uf_label === "gw_rssi"){
          label = "GW RSSI";
      }else{
          label = uf_label.replace(/_/g, " ");
      }
      return label;
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
              value = uf_val + '% RH';
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