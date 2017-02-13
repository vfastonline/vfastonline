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