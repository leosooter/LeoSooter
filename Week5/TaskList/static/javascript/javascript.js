$($(document).ready(function() {
  console.log("Jquery has loaded");
  updateTasks();

  $('.add_task').submit(function(){
    $.post('/tasks/new', $(this).serialize(), function(){
      $('.task_desc_add').val("");
      updateTasks();
    });
    console.log("Canceling reload from add_task");
    return false;
  });

  $('.delete_checked').click(function(){
    console.log("Deleting all completed tasks");
    $('.done:checked').each(function(){
      taskId = $(this).siblings('.task_id').val();
      form = $(this).parent('.task_display_form');
      deleteTask(form, taskId);
    });
  });

}));
//updateTasks function uses a Get request to refresh tasks on the page
function updateTasks(){
  console.log("Updating tasks");
  //Get request success function adds event listners to all dynamic content and
  //adds styling to completed tasks
  $.get('/tasks', function(tasks){
    $('.tasks_wrapper').empty();
    $('.tasks_wrapper').append(tasks);

    $('.task_display_form').submit(function(){
      console.log("Canceling reload from task_display_form");
      return false;
    });

    $('.update').click(function(){
      console.log("Updating Task Description");
      taskId = $(this).siblings('.task_id').val();
      console.log(taskId);
      $.post('/tasks/update/' + taskId, $(this).parent('.task_display_form').serialize(), function(tasks){
        console.log(tasks);
        updateTasks();
      });
    });

    $('.delete').click(function(){
      console.log("Deleting Task");
      taskId = $(this).siblings('.task_id').val();
      form = $(this).parent('.task_display_form');
      console.log(form);
      deleteTask(form, taskId);
    });

    $('.done').change(function(){
      if( $(this).prop('checked') === true ){
        taskId = $(this).siblings('.task_id').val();
        $.post('/tasks/complete/' + taskId + "/True", function(){
          updateTasks();
        });
      }
      else{
        taskId = $(this).siblings('.task_id').val();
        $.post('/tasks/complete/' + taskId + "/False", function(){
          updateTasks();
        });
      }
    });

    $('.done:not(:checked)').each(function(){
      console.log("styling un-checked");
      $(this).parent('.task_display_form').removeClass('checked');
      $(this).siblings('.task_desc_edit').prop('disabled', false);
      $(this).siblings('.update').prop('disabled', false);
    });

    $('.done:checked').each(function(){
      console.log("styling checked");
      $(this).parent('.task_display_form').addClass('checked');
      $(this).siblings('.task_desc_edit').prop('disabled', true);
      $(this).siblings('.update').prop('disabled', true);
    });
  //Closes out the success function for the Get request
  });

}

function deleteTask(form, id){
  $.post('/tasks/delete/' + id, function(tasks){
    console.log(tasks);
    updateTasks();
  });
}
