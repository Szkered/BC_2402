$(function() {
    $("#id_name").autocomplete({
	source: "/stocks/get_vendors/",
	minLength: 2,
	select: function( event, ui ) {
            $("#id_name").val(ui.item.name);
	    $("#id_address").val(ui.item.address);
	    $("#id_contact_no").val(ui.item.contact_no);
	    $("#id_email").val(ui.item.email);
	    $("#id_fax").val(ui.item.fax);
	    $("#id_contact_person_name").val(ui.item.contact_person_name);
	    return false;
        }
    });
});
