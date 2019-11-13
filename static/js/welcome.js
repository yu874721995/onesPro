
$(function() {
    $.post(hostUrl+'/session_test',function (data) {
                      console.log(data)
                      var s = JSON.parse(data).data.username;
                      var time = JSON.parse(data).data.time
                      $("#customerName").text(s);
                      $('#nowtime').text(time)
        }
    );
})