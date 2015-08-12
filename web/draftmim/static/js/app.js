'use strict';

angular.module('draftmim', ['draftmimServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/landing.html',
			controller: IndexController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
;
