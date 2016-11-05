$($(document).ready(function() {
  console.log("Jquery has loaded");
  //These are variables available anywhere in the function that will be modified and passed
  //as search parameters in the url
  var perPage = 10;
  var currentPage = 1;
  var orderBy = "leads_id";
  var sort = "ASC";
  var searchParams = "";
  //Creates a new Ajax call whenever search criteria is changed as per assignment
  //I think UI might be improved by adding an update button so that users can complete
  //their search criteria before starting a new search
  $('.search_criteria').change(function(){
    displayResults();
  });

  $('.per_page').change(function(){
    console.log("per_page change detected" + $(this).val());
    currentPage = 1;
    perPage = $(this).val();
    displayResults();
  });

  function displayResults(){
    searchParams = "";
    console.log("search_criteria change detected");
    var fName = $('#f_name').val();
    var lName = $('#l_name').val();
    var dateFrom = $('#from').val();
    var dateTo = $('#to').val();
    if (fName !== ""){
      searchParams += ("/" + fName + "%");
    }
    else searchParams += "/%";
    if (lName !== ""){
      searchParams += ("/" + lName + "%");
    }
    else searchParams += "/%";
    if (dateFrom !== ""){
      searchParams += ("/" + dateFrom);
    }
    else searchParams += "/2000-01-01";
    if (dateTo !== ""){
      searchParams += ("/" + dateTo);
    }
    else searchParams += "/" + getCurrentDate();
    //adds the order by, sort, current page and the number of results per page into the url and sends a get request
    searchParams += ( "/" + orderBy + "/" + sort + "/" + currentPage + "/" + perPage );
    console.log("searchParams =" + searchParams);
    $.get('/search' + searchParams, function(results){
      $('.results_wrapper').empty();
      $('.results_wrapper').append(results);
      addEvents();
    }, 'html');

  }
  //Add event listeners for dynamic content
  function addEvents(){
    $('.page_link').click(function(){
      console.log("link clicked " + $(this).text() );
      currentPage = $(this).text();
      displayResults();
    });


    console.log("Adding sort icon");
    console.log("orderBy = " + orderBy + "current order by = " + $('#' + "first_name").text() );
    if(sort === 'ASC'){
      $('#' + orderBy).append('<img src="static/images/down.png" alt="Down Arrow" />');
    }
    else{
      $('#' + orderBy).append('<img src="static/images/up.png" alt="Up Arrow" />');
    }

    $('.page_link').each(function(){
      if($(this).text() == currentPage){
        $(this).addClass('current_page');
      }
    });

    //Changes the order by and sort variables when the user click on column name
    $('.column_name').click(function(){
      console.log("changing order by");
      //If order by is already equal to column name- change the sort order
      if( orderBy === $(this).attr('id')){
        if(sort === 'ASC'){
          sort = 'DESC';
        }
        else{
          sort = 'ASC';
        }
      }
      //If order by is not equal to column name- default to ASC for the first sort
      else{
        sort = 'ASC';
      }
      //Set order by to the id of the column name
      orderBy = $(this).attr('id');
      displayResults();
    });
  }
  function getCurrentDate(){
    var currDate = new Date();
    dateString = currDate.getFullYear() + "-" + currDate.getMonth() + "-" + currDate.getDate();
    return dateString;
  }
}));// End of onload function
