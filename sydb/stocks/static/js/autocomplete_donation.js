$(function() {
    $("#id_name").autocomplete({
	source: "/stocks/get_donors/",
	minLength: 2,
	select: function( event, ui ) {
            $("#id_name").val(ui.item.name);
	    $("#id_address").val(ui.item.address);
	    $("#id_contact_no").val(ui.item.contact_no);
	    $("#id_mailing").attr("checked", ui.item.mailing);
	    $("#id_referral").val(ui.item.referral);
	    return false;
        }
    });
});
