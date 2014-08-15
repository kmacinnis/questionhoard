


function notify (event) {
    event.preventDefault();
    alert($(this).attr("id") );
}


function openAddForm (event) {
    event.preventDefault();
    $('#tabletop').load($(this).data("formurl"));
    $('#tabletop').data('currentAction','add');
    
}


function openEditForm (event) {
    event.stopPropagation();
    var link_id = this.attributes["id"].value;
    var stuff = link_id.split('-');
    var item_id = stuff.pop();
    var item_type = stuff.pop();
    $('#tabletop').load("/organization/"+ item_type + "/" + item_id + "/edit/");
    $('#tabletop').data('currentLabel','label-' + item_type + '-' + item_id);
    $('#tabletop').data('currentAction','edit');
    
}

function clearTabletop (event) {
    $('#tabletop').html("");
    $('#tabletop').removeData('currentLabel');
    $('#tabletop').removeData('currentAction');
}

function submitEdit (event) {
    var newName = this.name.value;
    var url = this.action;
    var data = $( this ).serialize();
    $.post(url, data, 
        function(data,status){
            if (data == 'success') {
                $('#'+$('#tabletop').data('currentLabel')).html(newName);
                clearTabletop();
            }
            else {
                $('#tabletop').html(data);
            }
        }
    );
}

function submitForm (event) {
    event.preventDefault();
     action = $('#tabletop').data('currentAction');
    var url = this.action;
    var data = $( this ).serialize();
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        dataType: 'json',
        success: function (response, status){
            if (response.success) {
                if (action == 'edit') {
                    $(response.label).html(response.name);
                } else if (action == 'add') {
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




$(document).ready(function () {
    $('#schema-accordions').on("click", ".item-edit", openEditForm);
    $('#schema-accordions').on("click", ".add-item", openAddForm);

    $('#tabletop').on("click", ".form-cancel", clearTabletop);
    $('#tabletop').on( "submit", "form", submitForm);
    
})
