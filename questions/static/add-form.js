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

};


function addquestion (event) {
    event.preventDefault();
    var link_id = this.attributes["id"].value;
    var question_id = link_id.split('-')[2];
    var count = $('.blockform').length; 
    $("#sortable").append('<div class="ajax-placeholder"></div>');
    $(".ajax-placeholder").load("/practicedocs/")
    $(".ajax-placeholder").removeClass("ajax-placeholder");
    
}








$(document).ready(function () {
    $('.add-question').click(addquestion);
});


function dontusethis () {
    $('[id$="DELETE"]').parent().append('<a href="#" class="del-item">Delete</a>');
    $('[id$="DELETE"]').hide();
    $('.delete-header').hide();
    $('.del-item').click(delrow);    
}