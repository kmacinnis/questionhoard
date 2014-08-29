


function notify (event) {
    event.preventDefault();
    alert($(this).attr("id") );
}


function openAddForm (event) {
    event.preventDefault();
    $('#tabletop').load($(this).data("formurl"), function () {
        $('#id_name').focus();
    });
    $('#tabletop').data('currentAction','add');
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
    baa = this;
    panel = $(this).closest('.panel');
    $.ajax({
        type: "GET",
        url: this.href,
        success: function (response, status){
            $(panel).addClass('current-panel');
            $('#tabletop').html(response.form_html);
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
                panel.html(response.panel_html);
            } else {
                $(panel).addClass('current-panel');
                $('#schema-accordions').addClass('hidden');
                $('#error-spot').removeClass('hidden');
                $('#error-spot').html(response.error_html);
                $('#tabletop').html(response.form_html);
                $('#tabletop').data('currentAction','validate question');
            }
        }
    })
}

function clearTabletop (event) {
    if ('validate question' == $('#tabletop').data('currentAction')) {
        $('#schema-accordions').removeClass('hidden');
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
                clearTabletop();
            }
            else {
                $('#tabletop').html(response.form_html);
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
    $('#schema-accordions').on("click", ".item-edit", openEditForm);
    $('#schema-accordions').on("click", ".add-item", openAddForm);
    $('#schema-accordions').on("click", ".add-question", openQuestionForm);
    $('#schema-accordions').on("click", ".edit-question", openQuestionForm);
    $('#schema-accordions').on("click", ".item-delete", confirmDelete);
    $('#schema-accordions').on("click", ".validate-link", validateQuestion);
    
    $('#confirm-btn').on("click", actualDelete);

    $('#tabletop').on("click", ".form-cancel", clearTabletop);
    $('#tabletop').on( "submit", "form", submitForm);
    
})
