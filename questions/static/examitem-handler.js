
function addQuestionToExam(question_id) {
    question_style = $('#part-info').data('questionStyle');
    if ('mix' == question_style) {
        question_style = 'mc';
    }
    var send_data = {
        question_id : question_id,
        exampart_id : $('#part-info').data('partId'),
        question_style : question_style,
        space_after : $('#space-after').html(),
        order : $('.exam-item').length + 1
    };
    $.ajax({
        type: 'GET',
        url: '/exams/add_question_to_exam/',
        data: send_data,
        success: function (response, status){
            if (response.success) {
                $('#part-items').append(response.item_div);
            } else {
                alert(response.err_mess);
            }
        }
    });
}

function addQuestionToPool(question_id) {
    $("#empty-pool").remove();
    var question_name = $.trim($("#question-name-" + question_id).html());
    var line = "<li data-id=" + question_id + ">" + question_name + ' <a class="remove-from-pool" href="#">[Remove]</a></li>';
    $("#focus-pool-list").append(line);
}

function removeQuestionFromPool(event) {
    event.preventDefault();
    $(this).closest('li').remove();
}

function addQuestion (event) {
    event.preventDefault();
    var question_id = $(this).attr('id').split('-').pop();
    if ($("#focus-pool").data('active')) {
        addQuestionToPool(question_id);
    } else {
        addQuestionToExam(question_id);
    }
}

function removeItem(event) {
    event.preventDefault();
    var item_id = $(this).data('itemId');
    var item_div = $(this).closest('.exam-item');
    $.ajax({
        type: 'GET',
        url: '/exams/remove_item_from_exam/',
        data: {item_id : item_id},
        success: function (response, status){
            if (response.success) {
                item_div.remove();
            } else {
                alert(response.err_mess);
            }
        }
    });
}

function changeSpaceAfter(event) {
    event.preventDefault();
    if ($('#space-after').data('changing')) {
        var newValue = $('#space-after-box').val();
        $('#space-after').html(newValue);
        $('#space-after').data('changing', false);
    } else {
        var oldValue = $('#space-after').html();
        var inputBox = '<input id="space-after-box" value="' + oldValue + '">';
        $('#space-after').html(inputBox);
        $('#space-after').data('changing', true);
    }
    
}

function showFocusPool(pool_id) {
    var send_data = {
        exampart_id : $('#part-info').data('partId'),
        pool_id : pool_id
    };
    $.ajax({
        type: 'GET',
        url: '/exams/pool/',
        data: send_data,
        success: function (response, status){
            $('#focus-pool').html(response.form);
            $("#focus-pool").removeClass("hidden");
            $("#part-items").addClass("hidden");
            $(".instructions").addClass("hidden");
            $(".add-question").html("Add to pool");
            $("#focus-pool").data('active', true);
            $("#focus-pool").data('pool_id', pool_id);
        }
    });
}

function saveFocusPool(event) {
    event.preventDefault();
    event.stopPropagation();
    $("#id_order").val($('.exam-item').length + 1);
    var k =  $("#focus-pool-list").children();
    var question_list = $(k).map(function (i, elem) {return $(elem).data("id");}).get();
    $("#id_questions").val("[" + question_list + "]");
    send_data = $(this).serializeArray();
    send_data.push({name: 'pool_id', value: $("#focus-pool").data('pool_id') });
    send_data.push({name: 'part_id', value: $('#part-info').data('partId') });
    send_data.push({name: 'question_list', value: question_list });
    
    $.ajax({
        type: 'POST',
        url: '/exams/pool/',
        data: send_data,
        success: function (response, status){
            if (response.submitted) {
                $('#part-items').append(response.item_div);
                hideFocusPool(event);
            } else {
                $('#focus-pool').html(response.form);
            }
        }
    });
}

function editItem(event) {
    event.preventDefault();
    event.stopPropagation();
    var url = $(this).attr('href');
    var item_type = $(this).data('itemType');
    var item_id = $(this).data('itemId');
    if (item_type == 'question') {
        $.ajax({
            type: 'GET',
            url: url,
            data: send_data,
            success: function (response, status) {
                if (response.success) {
                    $(this).closest('.exam-item').html(response.form);
                }
            }
        })
    } else if (item_type == 'pool') {
        showFocusPool(item_id);
    }
}

function newQuestionPool(event) {
    event.preventDefault();
    showFocusPool('new');
}

function hideFocusPool(event) {
    event.stopPropagation();
    event.preventDefault();
    $("#focus-pool").addClass("hidden");
    $("#part-items").removeClass("hidden");
    $(".instructions").removeClass("hidden");
    $(".add-question").html("Add to exam");
    $("#focus-pool").data('active', false);
}



$(document).ready(function () {
    $('#accordion-main').on("click", ".add-question", addQuestion);
    $('#part-items').on("click", ".remove-item", removeItem);
    $('#part-items').on("click",".edit-item", editItem);
    $("#change-space-after").click(changeSpaceAfter);
    $("#new-question-pool").click(newQuestionPool);
    $("#focus-pool").on("click",".remove-from-pool", removeQuestionFromPool);
    $('#focus-pool').on("click", ".form-cancel", hideFocusPool);
    $('#focus-pool').on("submit", "form", saveFocusPool);
    
});


