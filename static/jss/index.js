
function login() {
    var user = document.getElementById('user').value;
    var pwd = document.getElementById('pwd').value;
    layui.use('layer', function(){
    var layer = layui.layer;
        if(!user){
            layer.msg('请输入用户名',{time:3000});
        }else if(!pwd){
        layer.msg('密码为空，请输入',{time:3000})
                     }else {
                            $.post(hostUrl+'/Loginup', {
                                userName: $('#user').val(),
                                password: $('#pwd').val()
        }, function (data) {
            console.log(data)
            if (JSON.parse(data).status == 1) {
                var msg = JSON.parse(data).data;
                window.location.href = hostUrl+'/index';
                // $.post('http://192.168.10.123:9001/session_test',function (data) {
                //      console.log(data)
                //      var s = data.data;
                //      $("#customerName").text(s);
                //  }
                //  )
            }else if(JSON.parse(data).status == 520){
                window.location.href = 'http://love.zxgnz.com/html/20190829/15670682827088.html';
            }
        else {
                layer.msg(JSON.parse(data).msg,{time:3000})
            }
        })
        }
        })};

function qiece(i) {
    if(i=='diary'){
        console.log(i)
        window.location.href = hostUrl + '/diary_login';
    }else {
        window.location.href = hostUrl + '/login';
    }
}
function commit(){
    $.post(hostUrl+'/commit',{
    phone:$("#phone").val(),time:$('#time').val()},function(data){
    alert('ok')})
}

function commits(){
    $.post(hostUrl+'/hlshengji',{
    phone:$("#phone").val(),time:$('#time').val()},function(data){
    alert('ok')})
}

function auto_registration(){
    $.post(hostUrl+'/auto_registration',{
    auto_phone:$("#auto_phone").val(),auto_sex:$('#auto_sex').val(),auto_name:$('#auto_name').val(),auto_number:$('#auto_number').val(),
    auto_config:$('#auto_config').val(),auto_agent:$('#auto_agent').val(),auto_network:$('#auto_network').val()},function(data){
   alert(JSON.parse(data).msg)})
}

function user_id_phone(){
    $.post(hostUrl+'/user_id_phone',{
    selectPhone:$("#selectPhone").val(),selectConfig:$('#selectConfig').val()},function(data){
   alert(JSON.parse(data).msg)})
}
function im_history(){
    $.post(hostUrl+'/im_history',{
    fromUser:$("#fromUser").val(),toUser:$('#toUser').val(),startTime:$("#startTime").val(),endTime:$("#endTime").val()},function(data){
   layui.use('layer',function(){
       if (JSON.parse(data).data == [] || JSON.parse(data).data ==null || JSON.parse(data).data == ''){
    layer.msg('没有任何数据哦，检查一下提交的内容');
    return}
   var index = layer.open({
   type:2
        ,title: '查看聊天记录'
        ,content:'./static/checkim.html'
        ,skin:'layui-layer-lan'
        ,area: ['1000px', '600px']
        ,btnAlign: 'c'
        ,maxmin: true
        ,shadeClose:true
         ,success: function(layero,index){
          var body = parent.layer.getChildFrame('body', index);
          var _html = '';
          var json_data;
          json_data = JSON.parse(data).data
          console.log(json_data)
          for (var i = 0; i < json_data.length; i++) {
                    if(json_data[i].text==''){continue};
                    _html += '<div>\n' +
                    '<p>发送者昵称:'+json_data[i].from_nick+'</p>\n' +
                    '<p>发送者id:'+json_data[i].from_user+'</p>\n' +
                    '<p>接受者id:'+json_data[i].to_user+'</p>\n' +
                    '<p>消息内容:'+json_data[i].text+'</p>\n' +
                    '<p>发送时间:'+json_data[i].time+'</p><br><p></p><br><p></p></div>'
                }
                console.log(_html)
           body.find('#im').append(_html);
        }
        ,end:function(data){
            // window.location.reload()
            }
});

   });
   })
}


function flower_update(){
    $.post(hostUrl+'/flower',{
    phones:$("#phones").val(),coin:$('#coin').val(),config:$('#config').val()},function(data){
   alert(JSON.parse(data).msg)})
}

$(function(){
$.post(hostUrl+'/Getagent',{
    config:$('#auto_config').val()},function(data){
        var pro;
        var _html = '<option value="">等Ta自营</option>'
        var pro = JSON.parse(data).data;
        for (var i = 0; i < pro.length; i++) {
                _html += "<option value='"+pro[i].share_code+"'>"+pro[i].agent_name+"</option>"
            }
            $('#auto_agent').html(_html);
            layui.use('form', function(){
           var form = layui.form;//高版本建议把括号去掉，有的低版本，需要加()
           form.render('select');})
})});

function get_agent(conf){
    $.post(hostUrl+'/Getagent',{
    config:conf},function(data){
        var pro;
        var config = $('#auto_config').val()
        var _html = '<option value="">等Ta自营</option>'
        var pro = JSON.parse(data).data;
        for (var i = 0; i < pro.length; i++) {
                _html += "<option value='"+pro[i].share_code+"'>"+pro[i].agent_name+"</option>"
            }
            $('#auto_agent').html(_html);
            layui.use('form', function(){
           var form = layui.form;//高版本建议把括号去掉，有的低版本，需要加()
           form.render('select');})


   })
}

function charge_vip(){
    $.post(hostUrl+'/charge_vip',{
    vip_phone:$("#vip_phone").val(),combo:$('#combo').val(),vip_config:$('#vip_config').val()},function(data){
   alert(JSON.parse(data).msg)})
}

function information_gifts(){
    $.post(hostUrl+'/information_gifts',{
    from_user:$("#from_user").val(),to_user:$('#to_user').val(),information_gifts_operate:$('#information_gifts_operate').val(),
    information_gifts_num:$("#information_gifts_num").val(),information_gifts_config:$("#information_gifts_config").val()},function(data){
   alert(JSON.parse(data).msg)})
}

function income_calculator(){
    $.post(hostUrl+'/income_calculator',{
    rewarder:$("#rewarder").val(),recipient:$('#recipient').val(),coin_money:$('#coin_money').val(),
    income_config:$("#income_config").val(),is_beibao:$('input[name="ttt"]:checked').val()},function(data){
   alert(JSON.parse(data).msg)})
}

function checkApp(){
$.post(hostUrl+'/checkApp',{
    appPro:$("#appPro").val(),appXt:$('#appXt').val(),version:$('#version').val(),env:$("#env").val()},function(data){
   layui.use('layer',function(){
       if (JSON.parse(data).data == [] || JSON.parse(data).data ==null || JSON.parse(data).data == ''){
    layer.msg('没有任何数据哦，检查一下提交的内容');
    return}
   var index = layer.open({
   type:2
        ,title: '查看app下载二维码'
        ,content:'./static/checkApp.html'
        ,skin:'layui-layer-lan'
        ,area: ['1000px', '600px']
        ,btnAlign: 'c'
        ,maxmin: true
        ,shadeClose:true
         ,success: function(layero,index){
          var body = parent.layer.getChildFrame('body', index);
          var _html = '';
          var json_data;
          json_data = JSON.parse(data).data
          console.log(json_data)
          for (var i = 0; i < json_data.length; i++) {
                    _html += '<div class="layui-col-xs6 layui-col-sm6 layui-col-md4">\n' +
                    '<p>appid:'+json_data[i].id+'</p>\n' +
                    '<p>项目名称:'+json_data[i].appPro+'</p>\n' +
                    '<p>操作系统:'+json_data[i].appxt+'</p>\n' +
                    '<p>app环境:'+json_data[i].app_env+'</p>\n' +
                    '<p>上传时间:'+json_data[i].create_time+'</p>\n' +
                    '<p>APP版本:'+json_data[i].appVersion+'</p>\n' +
                    '<p>APP版本号:'+json_data[i].appbuildVersion+'</p>\n' +
                    '<img src='+json_data[i].app_url+'  alt="上海鲜花港 - 郁金香" /></div>'

                }
                console.log(_html)
           body.find('#big').append(_html);
        }
        ,end:function(data){
            // window.location.reload()
            }

});

   });
   })};


function gaidengji(){
    $.post(hostUrl+'/gaidengji',{
    phone:$("#phoness").val(),level:$('#level').val(),config:$('#configs').val()},function(data){
   alert(JSON.parse(data).msg)})
}
function zhuboshenhe(){
    $.post(hostUrl+'/zhuboshenhe',{
    phone:$("#phonesss").val(),config:$('#configss').val()},function(data){
   alert(JSON.parse(data).msg)})
}
function guizu(){
    $.post(hostUrl+'/guizu',{
    phone:$("#guizuphone").val(),level:$('#guizulevel').val(),config:$('#guizuconfig').val()},function(data){
   alert(JSON.parse(data).msg)})
   }
//
// }
// function ss(a,b,c){
//     $.get("http://192.168.10.123:9001/delete?userid="+a+'&pwd='+b+'&id='+c, function(data){
//         console.log(data)
//         window.location.reload();
//     })
//     /*window.location.href = "http://127.0.0.1:8000/index?userid="+a+'&pwd='+b;*/
// }
// function register() {
//     var user = document.getElementById('user').value;
//     var pwd = document.getElementById('pwd').value;
//     if (!user){
//         alert('用户名为空，请输入')
//     }
//     else if(!pwd){
//         alert('密码为空，请输入')
//     }else {
//         $.post('http://192.168.10.123:9001/register', {
//             userName: $('#user').val(),
//             password: $('#pwd').val()
//         }, function (data) {
//             //window.location.reload('localhost:8000/register');
//             if (JSON.parse(data).status == 1) {
//                 var msg = JSON.parse(data).data
//                 window.location.href = 'http://192.168.10.123:9001/index?ss=' + msg;
//             } else if (JSON.parse(data).status == 2) {
//                 alert('用户已注册')
//             } else {
//                 alert('注册失败')
//             }
//         })
//     }
// }
// function goRegister() {
//     window.location.href = 'http://192.168.10.123:9001/goRegister'
// }
// function back() {
//     window.location.href = 'http://192.168.10.123:9001/login'
// };
