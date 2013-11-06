$(function() {
    $("#id_name").autocomplete({
	source: "/stocks/get_vendors/",
	minLength: 2,
	select: function( event, ui ) {
            $("#id_name").val(ui.item.name);
	    $("#id_address").val(ui.item.address);
	    $("#id_contact_no").val(ui.item.contact_no);
	    return false;
        }
    });
});
