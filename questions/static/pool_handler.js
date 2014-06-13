function removequestion (event) {
    event.preventDefault();
    var question = $(this).closest(".pool-question");
    var link_id = $(this).attr("id");
    var question_id = link_id.split('-')[2];
    var pool_id = $("#pool-id").text();
    if (document.getElementById("question-"+ question_id)) {
      request_data = {
          'question_id': question_id,
          'pool_id': pool_id,
      };
      $.get( "/exams/ajax_remove_question_from_pool/", 
          request_data,
          function (response) {
              if (response === "success") {
                  question.remove()
              }
          }
      );
    }
    else {
        alert("This question is not in the pool.");
    }
    
    
}


function addquestion (event) {
    event.preventDefault();
    var link_id = this.attributes["id"].value;
    var question_id = link_id.split('-')[2];
    var pool_id = $("#pool-id").text();
    ifcondition = document.getElementById("question-"+ question_id)
    if (document.getElementById("question-"+ question_id)) {
        alert("This question is already in the pool.")
    }
    else {
      request_data = {
          'question_id': question_id,
          'pool_id': pool_id,
      };
      // $("#pool-question-list").append('<div class="ajax-placeholder">placeholder</div>');
      $.get( "/exams/ajax_add_question_to_pool/", 
          request_data,
          function (response) {
              $("#pool-question-list").append(response);
              $('.remove-question').click(removequestion);
          }
      );
    }
}







$(document).ready(function () {
    $('.add-question').click(addquestion);
    $('.remove-question').click(removequestion);
})
