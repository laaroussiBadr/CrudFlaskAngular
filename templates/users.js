var app = angular.module('myApp', []);

app.controller('PostCtrl', function($scope, $http) {
    $http.get("http://127.0.0.1:5000/api/post")
    .success(function(response) {
    	$scope.posts = response.objects;
    })
    .error(function(response) 
    	{
    		console.log(response);
    	});
  });


app.controller('Post', function($scope, $http) {
	$scope.text = "";
	$scope.title = "";
	$scope.date = new Date();

	$scope.submit = function() {
		var parameter = JSON.stringify({title:$scope.title, text:$scope.text, date:$scope.date, user_id:"1"});

		$http.post("http://127.0.0.1:5000/api/post",parameter)
		.success(function(response) {

    	})
		.error(function(response)
		{
			console.log(response);
		});
	}
  });