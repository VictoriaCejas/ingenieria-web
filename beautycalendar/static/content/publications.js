$(function(){

    var ClickLike= function() {
        var publication='{{publication.id}}'
        var likes=document.getElementById('Tlikes').textContent
        likes= parseInt(likes) + 1

         $.ajax({
             url:'{% url "like" pk=111%}'.replace('111',publication),
             type:'json',
             method:'GET',
             success: function like(data){
                 if (data.is_valid){
                    alert('like hecho'),
                    $('#Tlikes').text(likes + ' Likes');
                    $('#like').attr('disabled',true);
                    $('#dislike').attr('disabled',false);

                }
                else{
                    alert('ya habias dado like')
                }
           }

         })
        };

    var ClickDislike= function() {
        var publication='{{publication.id}}'
        var dislikes=document.getElementById('Tdislikes').textContent
        dislikes= parseInt(dislikes) - 1

         $.ajax({
             url:'{% url "dislike" pk=111%}'.replace('111',publication),
             type:'json',
             method:'GET',
             success: function like(data){
                 if (data.is_valid){
                    alert('dislike hecho'),
                    $('#Tdislikes').text(dislikes + ' Dislikes');
                    $('#dislike').attr("disabled", true);
                    $('#like').attr('disabled',false);

                    }
                else{
                    alert('ya habias dado dislike')
                }
             }

         })
        };

        var Carga= function() {
        var publication= '{{ publication.id }}'
        $.ajax({
            url:'{% url "totalLikes" pk=111 %}'.replace('111',publication),
            typle:'json',
            method:'GET',
            success: function totals(data){
                $('#Tlikes').text(data.positives + ' Likes'),
                $('#Tdislikes').text(data.negatives+' Dislikes')
            }
        })
      };

      document.addEventListener('DOMContentLoaded',Carga());
      $("#like").click(ClickLike);
      $("#dislike").click(ClickDislike);


});


