

(function(){
        $.post(hostUrl+'/Project',{},function (data) {
                  var _html,json_data;
                  json_data = JSON.parse(data).data
                  for (var i = 0; i < json_data.length; i++) {
                            _html += "<option value='"+json_data[i].id+"'>"+json_data[i].name+"</option>"
                        }
                        $('#project_id').append(_html);
              })})()