


function notify (event) {
    event.preventDefault();
    alert($(this).attr("id") );
}




function addRow (event) {
    event.preventDefault();
    var button_id = this.attributes["id"].value;
    var item = button_id.split('-')[1];
    var count = $('#' + item + '-table tbody').children().length;
    var template_code = $('#' + item +'-template').html();
    var new_row_code = template_code.replace(/__prefix__/g, count);
    
    $("#" + item + "-table tbody").append(new_row_code);
    $('#id_' + item + '-TOTAL_FORMS').attr('value', count+1);
    var delbox = $("#id_" + item + "-" + count + "-DELETE");
    delbox.parent().append('<a href="#" class="del-row">Delete</a>');
    delbox.hide();
    $('.del-row').click(delrow);

}

function delRow (event) {
    event.preventDefault();
    var thisrow = $(this).closest("tr");
    var rowid = thisrow.attr("id");
    var rowidsplit = rowid.split('-');
    var item = rowidsplit[1];
    var item_num = rowidsplit[2];
    $("#id_" + item + "-" + item_num + "-DELETE").attr('checked',true);
    thisrow.hide();
}


function toggleViewShortWell (event) {
    event.preventDefault();
    var shortwell = $("#well-prompt-short")
    if ($(shortwell).hasClass("hidden")) {
        $(shortwell).removeClass("hidden");
        $(this).html("Hide prompt & short version");
    }
    else {
        $(shortwell).addClass("hidden");
        $(this).html("Show prompt & short version");
    }
}

function readyQuestionForm () {
    $('.add-row').click(addRow);
    $('[id$="DELETE"]').parent().append('<a href="#" class="del-row">Delete</a>');
    $('[id$="DELETE"]').hide();
    $('.delete-header').hide();
    $('.del-row').click(delRow);
    $("#toggle-well-prompt-short").click(toggleViewShortWell);
}


function openAddForm (event) {
    event.preventDefault();
    $('#tabletop').load($(this).data("formurl"), function () {
        $('#id_name').focus();
    });
    $('#tabletop').data('currentAction','add');
}

function duplicateQuestion (event) {
    event.preventDefault();
    panel = $(this).closest('.panel');
    $.ajax({
        type: "GET",
        url: this.href,
        success: function (response, status){
            $(panel).addClass('current-panel');
            $('#tabletop').html(response.form_html);
            readyQuestionForm();
            for (i in response.formset_data) {
                fdata = response.formset_data[i];
                $(fdata.id).val(fdata.value);
            }
            $('#id_name').focus();
        }
    })
}


function openEditForm (event) {
    // event.stopPropagation();
    event.preventDefault();
    var link_id = this.attributes["id"].value;
    var stuff = link_id.split('-');
    var item_id = stuff.pop();
    var item_type = stuff.pop();
    $('#tabletop').load("/organization/"+ item_type + "/" + item_id + "/edit/");
    $('#tabletop').data('currentLabel','label-' + item_type + '-' + item_id);
}

function openQuestionForm (event) {
    event.preventDefault();
    panel = $(this).closest('.panel');
    $.ajax({
        type: "GET",
        url: this.href,
        success: function (response, status){
            $(panel).addClass('current-panel');
            $('#tabletop').html(response.form_html);
            readyQuestionForm();
            $('#id_name').focus();
        }
    })
}


function validateQuestion(event) {
    event.preventDefault();
    $('#tabletop').data('currentAction','validate question');
    var url = this.href;
    var panel = $(this).closest('.panel');
    $.ajax({
        type: "GET",
        url: url,
        data: 'ajax',
        success: function (response,status){
            if (response.validated){
                panel.replaceWith(response.panel_html);
                // TODO: Probably want to change this to just
                // typeset the reloaded content:
                MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            } else {
                $(panel).addClass('current-panel');
                $('#book-accordions').addClass('hidden');
                $('#error-spot').removeClass('hidden');
                $('#error-spot').html(response.error_html);
                $('#tabletop').html(response.form_html);
                readyQuestionForm();
                $('#tabletop').data('currentAction','validate question');
            }
        }
    })
}

function clearTabletop (event) {
    if ('validate question' == $('#tabletop').data('currentAction')) {
        $('#book-accordions').removeClass('hidden');
        $('#error-spot').addClass('hidden');
        $('#error-spot').html('');
    };
    $('#tabletop').html("");
    $('#tabletop').removeData('currentLabel');
    $('#tabletop').removeData('currentAction');
    $('#tabletop').removeData('currentPanel');
    $('.current-panel').removeClass('current-panel');
}

function submitForm (event) {
    event.preventDefault();
    var url = this.action;
    var data = $( this ).serialize();
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        dataType: 'json',
        success: function (response, status){
            if (response.success) {
                if (response.action == 'edit') {
                    $(response.label).html(response.name);
                } else if (response.action == 'add') {
                    $(response.place).append('<div id="ajax-placeholder">placeholder</div>');
                    $("#ajax-placeholder").replaceWith(response.panel_html);
                } else if (response.action == 'edit question') {
                    $('.current-panel').replaceWith(response.panel_html);
                } else if (response.action == 'validate question') {
                    $('.current-panel').replaceWith(response.panel_html);
                }
                // TODO: Probably want to change this to just
                // typeset the newly loaded content:
                MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
                clearTabletop();
            }
            else {
                $('#tabletop').html(response.form_html);
                readyQuestionForm();
                if ($('#tabletop').data('currentAction') == 'validate question') {
                    $('#error-spot').html(response.error_html);                    
                }
            }
        },
    });
}

function confirmDelete (event) {
    event.stopPropagation();
    event.preventDefault();
    var data = $(this).data();
    $('#delete-item-type').html(data.itemType);
    $('#delete-item-name').html(data.itemName);
    $("#confirm-delete").modal();
    $("#confirm-btn").data('url', data.confirmedUrl);
    $("#confirm-btn").data('panel', $(this).closest('.panel'));
}

function actualDelete (event) {
    var data = $(this).data();
    $("#confirm-delete").modal("hide");
    $.ajax({
        type: "GET",
        url: data.url,
        data: {confirmed:true},
        success: function (response, status){
            if (response == 'deleted') {
                data.panel.remove();
            } else {
                alert("An unknown error occurred.");
            }
        },
        error: function  (jqXHR, textStatus, errorThrown) {
            alert(textStatus);
        }
    })
}



$(document).ready(function () {
    $('#book-accordions').on("click", ".item-edit", openEditForm);
    $('#book-accordions').on("click", ".add-item", openAddForm);
    $('#book-accordions').on("click", ".add-question", openQuestionForm);
    $('#book-accordions').on("click", ".edit-question", openQuestionForm);
    $('#book-accordions').on("click", ".duplicate-question", duplicateQuestion);    
    $('#book-accordions').on("click", ".item-delete", confirmDelete);
    $('#book-accordions').on("click", ".validate-link", validateQuestion);
    
    $('#confirm-btn').on("click", actualDelete);

    $('#tabletop').on("click", ".form-cancel", clearTabletop);
    $('#tabletop').on( "submit", "form", submitForm);
    
    $('.collapse').on('shown.bs.collapse', function(){
    $(this).parent().find(".glyphicon-menu-right").removeClass("glyphicon-menu-right").addClass("glyphicon-menu-down");
    }).on('hidden.bs.collapse', function(){
    $(this).parent().find(".glyphicon-menu-down").removeClass("glyphicon-menu-down").addClass("glyphicon-menu-right");
    });
    
    
    
    
})
