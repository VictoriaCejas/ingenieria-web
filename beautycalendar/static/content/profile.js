$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-photo .modal-content").html("");
          $("#modal-photo").modal("show");
        },
        success: function (data) {
          $("#modal-photo .modal-content").html(data.html_form);
        }
      });
    };
  
    var saveForm = function () {
        var form = $(this);
        var fd= new FormData(this);

        $.ajax({
          url: form.attr("action"),
          data: fd,
          processData:false,
          contentType:false,
          type: form.attr("method"),
          dataType: 'json',
        success: function (data) {

          if (data.form_is_valid) {
            location.reload();

            $("#modal-photo").modal("hide");
          }
          else {
            $("#modal-photo .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    $(".js-update-photo").click(loadForm)
    $("#modal-photo").on("submit",".js-photo-update-form",saveForm)
   
  
  });