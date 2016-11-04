$($(document).ready(function() {
  console.log("Jquery has loaded");
  //Gets all notes from the DB and displays them on page load.
  $.get('/notes', function(notes) {
      resetNotes(notes);
  });
  //Add notes to DB
  $('.add_note').submit(function(){
    console.log("Add note form");
    $.post('/notes/new', $(this).serialize(), function(notes) {
      resetNotes(notes);
    });
    $("input[name='title']").val('');
    $("input[name='description']").val('');
    return false;
  });
}));

//Function serves to refresh the notes on the page and
//to add event listeners to any newly created dynamic content.
function resetNotes(note_data){
  $('.note_wrapper').empty();
  $('.note_wrapper').append(note_data);
  //Delete note
  $('.delete').submit(function(){
    console.log("Delete JS called");
    console.log($(this) );
    $.post('/notes/destroy/'+ $(this).children('.note_id').val(), $(this).serialize(), function(notes){
      resetNotes(notes);
    });
    console.log("canceling relaod");
    return false;
  });
  //Update note- form aslo displays the notes on the main page
  $('.note_display').submit(function(){
    console.log("Update JS called");
    console.log($(this) );
    $(this).children('.update_button').hide();
    $.post('/notes/update/'+ $(this).children('.note_id').val(), $(this).serialize(), function(notes){
      resetNotes(notes);
    });
    console.log("canceling relaod");
    return false;
  });
  //Unhides the update button if there are any changes to the note description
  $('.description').change(function(){
    $(this).siblings('.update_button').show();
  });
}
