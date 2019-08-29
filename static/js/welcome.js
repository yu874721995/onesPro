
$(function() {
    $.post('http://47.93.244.11:9001/session_test',function (data) {
                      console.log(data)
                      var s = JSON.parse(data).data.username;
                      var time = JSON.parse(data).data.time
                      $("#customerName").text(s);
                      $('#nowtime').text(time)
        }
    );
})