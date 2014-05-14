function addrow (event) {
    event.preventDefault();
    var button_id = this.attributes["id"].value;
    var item = button_id.split('-')[1];
    var count = $('#' + item + '-table tbody').children().length;
    var template_code = $('#' + item +'-template').html();
    var new_row_code = template_code.replace(/__prefix__/g, count);
    
    $("#" + item + "-table tbody").append(new_row_code);
    $('#id_' + item + '-TOTAL_FORMS').attr('value', count+1);
    var delbox = $("#id_" + item + "-" + count + "-DELETE");
    delbox.parent().append('<a href="#" class="del-item">Delete</a>');
    delbox.hide();
    $('.del-item').click(delrow);

}

function delrow (event) {
    event.preventDefault();
    var thisrow = $(this).closest("tr");
    var rowid = thisrow.attr("id");
    var rowidsplit = rowid.split('-');
    var item = rowidsplit[1];
    var item_num = rowidsplit[2];
    $("#id_" + item + "-" + item_num + "-DELETE").attr('checked',true);
    thisrow.hide();
}



$(document).ready(function () {
    $('.add-item').click(addrow);
    $('[id$="DELETE"]').parent().append('<a href="#" class="del-item">Delete</a>');
    $('[id$="DELETE"]').hide();
    $('.delete-header').hide();
    $('.del-item').click(delrow);
});
