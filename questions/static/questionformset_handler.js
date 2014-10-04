function delblock (event) {
    event.preventDefault();
    alert('in!');
    block = $(this).closest(".questionform");
    block_id = block.attr("id");
    $("#" + block_id + "-DELETE").attr('checked',true);
    block.hide();
}


function addblock (event) {
    event.preventDefault();
    var link_id = this.attributes["id"].value;
    var question_id = link_id.split('-')[2];
    var partrecipe_id = $("#part-recipe-id").text();
    var count = $('.questionform').length;
    var style = $("#id_question_style").val()
    $("#id_examrecipequestion_set-TOTAL_FORMS").attr('value',count+1);
    request_data = {
        'question_id': question_id,
        'partrecipe_id': partrecipe_id,
        'form_num': count,
        'style': style,
    };
    $("#sortable").append('<div class="ajax-placeholder">placeholder</div>');
    $.get( "/exams/new_erq_form/", 
        request_data,
        function (response) {
            $(".ajax-placeholder").html(response);
            $(".ajax-placeholder").removeClass("ajax-placeholder"); 
        }
    );
}







$(document).ready(function () {
    $('.add-question').click(addblock);
    $('.delete-block').click(delblock);
})


