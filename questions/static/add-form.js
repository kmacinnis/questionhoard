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

function delblock (event) {
    alert("This doesn't work yet.");
}


function addquestion (event) {
    event.preventDefault();
    var link_id = this.attributes["id"].value;
    var question_id = link_id.split('-')[2];
    var docrecipe_id = $("#doc-recipe-id").text();
    var count = $('.blockform').length;
    $("#id_blockrecipe_set-TOTAL_FORMS").attr('value',count+1);
    request_data = {
        'question_id': question_id,
        'docrecipe_id': docrecipe_id,
        'form_num': count
    };
    $("#sortable").append('<div class="ajax-placeholder">placeholder</div>');
    $.get( "/practicedocs/new_blockrecipe_form/", 
        request_data,
        function (response) {
            alert(response);
            $(".ajax-placeholder").html(response);
            $(".ajax-placeholder div.order").addClass("hidden");
            $(".ajax-placeholder").removeClass("ajax-placeholder"); 
        }
    );
}







$(document).ready(function () {
    $('.add-question').click(addquestion);
})


function dontusethis () {
    $('[id$="DELETE"]').parent().append('<a href="#" class="del-item">Delete</a>');
    $('[id$="DELETE"]').hide();
    $('.delete-header').hide();
    $('.del-item').click(delrow);    
}