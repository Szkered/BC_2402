$(function() {
    $("#id_name").autocomplete({
	source: "/stocks/get_destination/",
	minLength: 2,
	select: function( event, ui ) {
            $("#id_name").val(ui.item.name);
	    $("#id_person_in_charge").val(ui.item.person_in_charge);
	    $("#id_contact_no").val(ui.item.contact_no);
	    return false;
        }
    });
});
