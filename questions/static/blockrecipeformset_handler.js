function delblock (event) {
    event.preventDefault();
    var block = $(this).closest(".blockform");
    var block_id = block.attr("id");
    $("#" + block_id + "-DELETE").attr('checked',true);
    block.hide();
}


function addblock (event) {
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
            $(".ajax-placeholder").removeClass("ajax-placeholder"); 
        }
    );
}







$(document).ready(function () {
    $('.add-question').click(addblock);
    $('.delete-block').click(delblock);
})
