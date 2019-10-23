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
          if (window.location.pathname.indexOf("/profile/")==0){
            alert('Denuncia recibida!');
          }

        }
        else {
          $("#modal-photo .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */
  // $('#admin-table').DataTable();

  $(".js-update-photo").click(loadForm)
  $("#modal-photo").on("submit",".js-photo-update-form",saveForm)
  

});