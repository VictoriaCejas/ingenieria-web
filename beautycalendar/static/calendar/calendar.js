$(function () {

    /* Functions */
    
    var loadList = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'post',
        dataType: 'json',
        success: function (data) {
          $("#my-table .table-content").html(data.html_form);
        }
      });
    };
  
    
    /* Binding */
  
    // Create content
    $(".js-create-times").click(loadList);
  
  });
  