'use strict';

/* Filters */

angular.module('draftmimFilters', []).filter('uppercase', function() {
	return function(input) {
		return input.toUpperCase();
	}
});
