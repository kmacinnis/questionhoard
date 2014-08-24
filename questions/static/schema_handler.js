


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
    $('#tabletop').data('currentAction','edit');
    
}

function openQuestionForm (event) {
    event.preventDefault();
    $('#tabletop').load(this.href + ' form', function () {
        $('#id_name').focus();
    });
    $('#tabletop').data('currentAction','add');
}

function clearTabletop (event) {
    $('#tabletop').html("");
    $('#tabletop').removeData('currentLabel');
    $('#tabletop').removeData('currentAction');
}

function submitForm (event) {
    moo = this;
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
                }
                clearTabletop();
            }
            else {
                $('#tabletop').html(response.form_html);
            }
        },
    });
}

function confirmDelete (event) {
    event.stopPropagation();
    event.preventDefault();
    var data = $(this).data();
    moo = this;
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
    $('#schema-accordions').on("click", ".item-delete", confirmDelete);
    
    $('#confirm-btn').on("click", actualDelete);

    $('#tabletop').on("click", ".form-cancel", clearTabletop);
    $('#tabletop').on( "submit", "form", submitForm);
    
})
