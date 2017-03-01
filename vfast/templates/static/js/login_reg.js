var usernameCheck = false;
var emailCheck = false;
var passwordCheck = false;

function blur_username(t){
    if(check_name(t.value) == "error"){
        username_span.innerHTML = "用户名格式错误！";
        username_span.style.color = "red";
        usernameCheck = false;
    }else{
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("post","/u/exists",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                var jsonStr = JSON.parse(xmlhttp.responseText);
                if(jsonStr.code == "0"){
                    username_span.innerHTML = "用户名可以使用！";
                    username_span.style.color = "#4DB6AC";
                    usernameCheck = true;
                }else{
                    username_span.innerHTML = "用户名已被使用！";
                    username_span.style.color = "red";
                    usernameCheck = false;
                }
            }
        };
        xmlhttp.send("username="+t.value);
    }
}
function blur_email(t){
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
    if(reg.test(t.value)){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("post","/u/exists",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                var jsonStr = JSON.parse(xmlhttp.responseText);
                if(jsonStr.code == "0"){
                    email_span.innerHTML = "邮箱可以使用！";
                    email_span.style.color = "#4DB6AC";
                    emailCheck = true;
                }else{
                    email_span.innerHTML = "邮箱已被使用！";
                    email_span.style.color = "red";
                    emailCheck = false;
                }
            }
        };
        xmlhttp.send("email="+t.value);
    }else{
        email_span.innerHTML = "邮箱格式错误！";
        email_span.style.color = "red";
        emailCheck = false;
    }
}
function blur_password(t){
    if(t.value.replace(/\s/g, "")==""){
        password_span.innerHTML = "密码不能为空！";
        password_span.style.color = "red";
        passwordCheck = false;
    }else{
        passwordCheck = true;
    }
}
function check_name(str){
    var re1=/[a-zA-Z]|[0-9]/g;
    var re2=/[\u4e00-\u9fa5]/g;
    var length = 0;
    var length2 = 0;
    if (str.match(re1)) {
      var letter =  str.match(re1);
      length += letter.length;
      length2 += letter.length;
    }

    if (str.match(re2)) {
      var chinese = str.match(re2);
      length += chinese.length;
      length2 = length2+chinese.length*2;
    }

    if (length == str.length) {
        if (length2>=2 && length2<=10) {
            return 'success';
        }else{
            return 'error';
        }
    }else{
        return 'error';
    }
}
function reg_submit(){
    var username = $("#username").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var program_exp =$("input:radio[name='program_exp']:checked").val();
    var into_it =$("input:radio[name='into_it']:checked").val();
    var learn_habit =$("input:radio[name='learn_habit']:checked").val();
    var comp_use_time_day =$("input:radio[name='comp_use_time_day']:checked").val();
    var sex =$("input:radio[name='sex']:checked").val();

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("post","/u/register",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.onreadystatechange = function(){
        if(xmlhttp.readyState == 4 && xmlhttp.status==200){
            var jsonStr = JSON.parse(xmlhttp.responseText);
            if(jsonStr.code == "0"){
                var hash = {
                    'qq.com': 'http://mail.qq.com',
                    'gmail.com': 'http://mail.google.com',
                    'sina.com': 'http://mail.sina.com.cn',
                    '163.com': 'http://mail.163.com',
                    '126.com': 'http://mail.126.com',
                    'yeah.net': 'http://www.yeah.net/',
                    'sohu.com': 'http://mail.sohu.com/',
                    'tom.com': 'http://mail.tom.com/',
                    'sogou.com': 'http://mail.sogou.com/',
                    '139.com': 'http://mail.10086.cn/',
                    'hotmail.com': 'http://www.hotmail.com',
                    'live.com': 'http://login.live.com/',
                    'live.cn': 'http://login.live.cn/',
                    'live.com.cn': 'http://login.live.com.cn',
                    '189.com': 'http://webmail16.189.cn/webmail/',
                    'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
                    'yahoo.cn': 'http://mail.cn.yahoo.com/',
                    'eyou.com': 'http://www.eyou.com/',
                    '21cn.com': 'http://mail.21cn.com/',
                    '188.com': 'http://www.188.com/',
                    'foxmail.com': 'http://www.foxmail.com',
                    'outlook.com': 'http://www.outlook.com'
                }
                swal({
                    title: "注册成功！",
                    text: "激活邮件已经发送至您的邮箱，请前去激活！",
                    type: "success",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "邮箱激活",
                    cancelButtonColor: "#4DB6AC",
                    cancelButtonText: "完成",
                    closeOnConfirm: false
                },
                function(){
                    // 点击登录邮箱
                    var _mail = $("#email").val().split('@')[1];    //获取邮箱域
                    for (var j in hash){
                        if(j == _mail){
                            //跳转邮箱链接
                            window.open(hash[_mail],"_self");
                        }
                    }
                });
            }else{
                swal("错误！", "注册失败！", "warning");
            }
        }
    };
    var str = "username="+username+"&" +
            "email="+email+"&" +
            "password="+password+"&" +
            "program_exp="+program_exp+"&" +
            "into_it="+into_it+"&" +
            "learn_habit="+learn_habit+"&" +
            "comp_use_time_day="+comp_use_time_day+"&" +
            "sex="+sex;
    xmlhttp.send(str);
}
function login(){
    var username = $("#username").val().trim();
    var password = $("#password").val().trim();
    $("#usernameSpan").html("");
    $("#passwordSpan").html("");
    if(username != "" && password != ""){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("post","/u/login",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                var jsonStr = JSON.parse(xmlhttp.responseText);
                if(jsonStr.code == "0"){
                    console.log(jsonStr.url)
                    location.href = jsonStr.url;
                }else if(jsonStr.code == "1" || jsonStr.code == "2"){
                    $("#usernameSpan").html(jsonStr.msg);
                }else if (jsonStr.code = "3"){
                    $("#passwordSpan").html(jsonStr.msg);
                }
            }
        };
        var str = "username="+username+"&" +
                "password="+password;
        xmlhttp.send(str);
    }
}