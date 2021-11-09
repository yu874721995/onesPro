
function batchExecution() {
    var checkout = table.checkStatus('demo')
    var caseId = []
    if(checkout.data.length == 0){
        layer.msg('请选择用例')
        return false
    }
    for(var i=0;i<checkout.data.length;i ++){
        if(checkout.data[i].status == 0){
            layer.msg('包含已禁用的用例')
            return false
        }
        caseId.push(checkout.data[i].case_id)
    }
    console.log(caseId)
    $.post(hostUrl+'/batchExecution',{caseId:JSON.stringify(caseId)},function (data) {
        var json_msg = JSON.parse(data).msg
        layer.msg(json_msg)

    })
}
function open_Add(data){
        var query = data.data;
        var type = data.type;
        console.log(query,type)
        parent.layer.open({
        type:2
        ,title: '查看审核详情'
        ,content:'../static/shenhedata.html'
        ,skin:'layui-layer-lan'
        ,area: ['500px', '600px']
        ,btnAlign: 'c'
        ,maxmin: true
        ,shadeClose:true
         ,success: function(layero,index){
         var body = parent.layer.getChildFrame('body', index);
         var _html = ''

          if(type=='头像'){
                        _html += "<img src='"+query.avatar+"' style='width:500px'/>";
                        _html += "<h1 style='width:300px'>用户昵称："+query.name+"</h1>";
                        _html += "<h1 style='width:300px'>用户性别："+query.sex+"</h1>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",1)'>通过</span>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;'  onclick='shenhe("+JSON.stringify(data)+",2)'>不通过</span>";
                        };
          if(type=='动态'){
             var image = JSON.parse(query.images)
             var video = JSON.parse(query.video)
                for (var i = 0; i < image.length; i++) {
                            _html += "<img src='"+image[i].url+"' style='width:500px'/>";
                        };
                if(video.length != 0){_html += '<video width="400" height="240" controls="controls"><source src="'+video.url+'" type="video/mp4" /></video>';};
                        _html += "<h1 style='width:300px'>动态文案："+query.text+"</h1>";
                        _html += "<h1 style='width:300px'>用户昵称："+query.name+"</h1>";
                        _html += "<h1 style='width:300px'>用户性别："+query.sex+"</h1>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",1)'>通过</span>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",2)'>不通过</span>";
                        };
        if(type=='相册'){
                            _html += "<img src='"+query.pic+"' style='width:500px'/>";
                        _html += "<h1 style='width:300px'>用户昵称："+query.name+"</h1>";
                        _html += "<h1 style='width:300px'>用户性别："+query.sex+"</h1>";
                             _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",1)'>通过</span>";
                            _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",2)'>不通过</span>";
                        };

        if(type=='标签'){
                        _html += "<img src='"+query.avatar+"' style='width:500px'/>";
                        _html += "<h1 style='width:300px'>所选标签："+query.tag_text+"</h1>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",1,"+index+")'>通过</span>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",2,"+index+")'>不通过</span>";
                        };

        if(type=='真人认证'){
                        _html += "<img src='"+query.avatar+"' style='width:500px'/>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",1)'>通过</span>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",2)'>不通过</span>";
                        };

        if(type=='招呼'){
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",1)'>通过</span>";
                        _html += "<span class='layui-btn' style='height:100px;width:180px;font-size:50px;padding-top:30px;' onclick='shenhe("+JSON.stringify(data)+",2)'>不通过</span>";
                        $.post(hostUrl+'/zhaohu',{id:query.id},function (data) {
                        console.log(data)
                                _html = JSON.parse(data).data;
                                console.log(_html);
                                                    layer.open({
                                                    type : 1,
                                                    title : '招呼审核',
                                                    maxmin : true,
                                                    offset: '100px',
                                                    area : [ '400px', '500px' ],
                                                    content : _html,
                                                    end:function(data){
                                                            parent.layer.close(parent.layer.index);
                                                            }// iframe的url
                                                });
                            })
                        };
                        body.find('#shenheneirong').append(_html);
        }
        ,end:function(data){
            // window.location.reload()
            parent.location.reload();
            }
})}
function shenhe(data,status,index){
console.log(data.data.id);
console.log(status);
console.log(index);
$.post(hostUrl+'/shijishenhe',{id:data.data.id,status:status,type:data.type},function (data) {
        var json_msg = JSON.parse(data).msg

        if(json_msg=='审核成功'){

        parent.layer.close(parent.layer.index);
        parent.layer.msg(json_msg);

        }

    })
}


