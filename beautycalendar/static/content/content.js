$(function () {

  /* Functions */
  
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-mycontent .modal-content").html("");
        $("#modal-mycontent").modal("show");
      },
      success: function (data) {
        $("#modal-mycontent .modal-content").html(data.html_form);
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
          if (window.location.pathname.indexOf("/products/")==0){
          $("#mycontent-table tbody").html(data.html_product_list);
          }
          if (window.location.pathname.indexOf("/services/")==0){
            $("#mycontent-table tbody").html(data.html_service_list);
          }
          if (window.location.pathname.indexOf("/empleoyees/")==0){
            $("#mycontent-table tbody").html(data.html_empleoyee_list);
          }
          $("#modal-mycontent").modal("hide");
        }
        else {
          $("#modal-mycontent .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-mycontent").click(loadForm);
  $("#modal-mycontent").on("submit", ".js-mycontent-create-form", saveForm);

  // Update book
  $("#mycontent-table").on("click", ".js-update-mycontent", loadForm);
  $("#modal-mycontent").on("submit", ".js-mycontent-update-form", saveForm);

  // Delete book
  $("#mycontent-table").on("click", ".js-delete-mycontent", loadForm);
  $("#modal-mycontent").on("submit", ".js-mycontent-delete-form", saveForm);

});