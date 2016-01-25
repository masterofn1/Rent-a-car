(function(angular) {
  'use strict';

  angular
    .module('app.services')
    .service('HomeModel', homeModel)

  homeModel.$inject = [
    '$location',
    'loading',
    'LxDialogService',
    'LxNotificationService',
    'LxProgressService',
    'HomeREST',
    'store',
    '$q',
  ];

  function homeModel (location, loading, LxDialogService, LxNotificationService, LxProgressService, HomeREST, store, $q){
    angular.extend(this, active_user);
    LxProgressService.circular.show('primary', '#progress');

    this.loading = loading.new();
    this.isBusy = isBusy;
    this.activate = activate;
    this.search = search;
    this.query = {};
    this.diff_location = false;
    this.searchbox_show = true;
    this.search_results;
    this.times = [
      "12:00AM", "12:30AM", "1:00AM","1:30AM","2:00AM","2:30AM","3:00AM","3:30AM","4:00AM","4:30AM","5:00AM","5:30AM","6:00AM",
      "6:30AM","7:00AM","7:30AM","8:00AM","8:30AM","9:00AM","9:30AM","10:00AM","10:30AM","11:00AM","11:30AM","12:00PM",
      "12:30PM", "1:00PM","1:30PM","2:00PM","2:30PM","3:00PM","3:30PM","4:00PM","4:30PM","5:00PM","5:30PM",
      "6:00PM","6:30PM","7:00PM","7:30PM","8:00PM","8:30PM","9:00PM","9:30PM","10:00PM","10:30PM","11:00PM","11:30PM"
    ];

    function search(){
      var self = this;
      if(self.query.location===undefined||self.query.location===""){
        alert("Location required!");
      }else{
        self.loading.watch(HomeREST.search(self.query))
      .success(function(d){
        console.log(d);
        self.search_results = d;
        self.searchbox_show = false;
      })
      }

    }




    function activate(){

    }

    function isBusy() {
      return !!this.loading._futures.length;

    }


  }

})(window.angular);
