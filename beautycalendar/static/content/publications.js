$(function(){

    var publication=document.getElementById('pub-id').value

    var createComment= function(){
        var fd= new FormData(this);
        $.ajax({
            url:'{% url "save_comment" pk=111 %}'.replace('111',publication),
            type:'json',
            data: fd,
            method:'POST',
            success: function sincComments(data){
                if (data.is_valid){
                    document.getElementById("list-comments").appendChild(data.comment); 
                }
            }
        });
    };


    var like= function(){
        var likes=document.getElementById('Tlikes').textContent
        var dislikes=document.getElementById('Tdislikes').textContent
        likes= parseInt(likes) + 1
        dislikes= parseInt(dislikes)-1
            if (dislikes < 0){
                dislikes=0
            }
       $.ajax({
           url:'{% url "like" pk=111%}'.replace('111',publication),
           type:'json',
           method:'GET',
           success: function like(data){
               if (data.is_valid){
                  alert('like hecho'),
                  $('#Tlikes').text(likes + ' Likes');
                  $('#Tdislikes').text(dislikes + ' Dislikes');
                  $('#like').attr('disabled',true);
                  $('#dislike').attr('disabled',false);

              }
              else{
                  alert('ya habias dado like')
              }
         }

       });
    };

    var dislike= function() {
        var dislikes=document.getElementById('Tdislikes').textContent
        var likes=document.getElementById('Tlikes').textContent
        dislikes= parseInt(dislikes) + 1
        likes= parseInt(likes)-1
        if (likes<0){
            likes=0
        }
       $.ajax({
           url:'{% url "dislike" pk=111%}'.replace('111',publication),
           type:'json',
           method:'GET',
           success: function like(data){
               if (data.is_valid){
                  alert('dislike hecho'),
                  $('#Tdislikes').text(dislikes + ' Dislikes');
                  $("#Tlikes").text(likes+' Likes');
                  $('#dislike').attr("disabled", true);
                  $('#like').attr('disabled',false);

                  }
              else{
                  alert('ya habias dado dislike')
              }
           }

       });
    };
    
    // var Load=function() {
    //   $.ajax({
    //       url:'{% url "totalLikes" pk=111 %}'.replace('111',publication),
    //       typle:'json',
    //       method:'GET',
    //       success: function totals(data){
    //           $('#Tlikes').text(data.positives + ' Likes'),
    //           $('#Tdislikes').text(data.negatives+' Dislikes')
    //       }
    //   })
    // };

    $( "#dislike" ).on( "click",dislike);
    $( "#like" ).on( "click", like);
    $("#btn-comentario").on("click",createComment)
    
});


