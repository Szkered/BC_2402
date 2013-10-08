$(function(){
    $("#donors").autocomplete({
	source: "/api/donation/",
	minLength: 2,
    });
});
