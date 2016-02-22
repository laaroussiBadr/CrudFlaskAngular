var app = angular.module('myApp', []);

app.controller('MainCtrl', function($scope, $http) {
    $http.get("http://127.0.0.1:5000/api/post")
    .success(function(response) {
    	$scope.posts = response.objects;
    })
    .error(function(response) 
    	{
    		console.log(response);
    	});
  });