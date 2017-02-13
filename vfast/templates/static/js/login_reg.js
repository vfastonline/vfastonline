function blur_username(t){
    if(t.value.replace(/\s/g, "")==""){
        username_span.innerHTML = "用户名不能为空！";
        username_span.style.color = "red";
    }else{
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("post","/u/exists",true);
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                console.log(xmlhttp.responseText);
            }
        };
        xmlhttp.send("username="+ t.value);
    }
}
function blur_email(t){
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
    if(reg.test(t.value)){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("post","/u/exists",true);
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                console.log(xmlhttp.responseText);
            }
        };
        xmlhttp.send("email="+ t.value);
    }else{
        email_span.innerHTML = "邮箱格式不正确！";
        email_span.style.color = "red";
    }
}