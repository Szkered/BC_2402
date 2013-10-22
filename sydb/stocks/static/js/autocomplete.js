$(function() {
    $('[id$=stock_name]').autocomplete({
	source: "/stocks/get_stocks/",
	minLength: 2,
	select: function( event, ui ) {
	    $(this).val(ui.item.name);
	    $(this).parent().siblings().children('[id$=unit_price]').val(ui.item.unit_price);
            $(this).parent().siblings().children('[id$=unit_measure]').val(ui.item.unit_measure);
	    $(this).parent().siblings().children('[id$=category]').val(ui.item.categorys);
	    return false;
        }
    });
    $("#add").click(function(){
	$('[id$=stock_name]').autocomplete({
	    source: "/stocks/get_stocks/",
	    minLength: 2,
	    select: function( event, ui ) {
		$(this).val(ui.item.name);
		$(this).parent().siblings().children('[id$=unit_price]').val(ui.item.unit_price);
		$(this).parent().siblings().children('[id$=unit_measure]').val(ui.item.unit_measure);
		return false;
            }
	});	
    });
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
 
    $('[id$=category]')
      // don't navigate away from the field on tab when selecting an item
      .bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).data( "ui-autocomplete" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "/stocks/get_categorys/", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 2 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
});
