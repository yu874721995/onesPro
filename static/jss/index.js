
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
gaihuahua

function gaihuahua(){
    $.post(hostUrl+'/gaihuahua',{
    phones:$("#phones").val(),coin:$('#coin').val(),config:$('#config').val()},function(data){
   alert(JSON.parse(data).msg)})
}
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
