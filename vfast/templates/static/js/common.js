$(function(){
	$("body").css("opacity","1");
	$(".slideDIV").slideUp(350);
	if($("#uid").val() != ""){
        $.getJSON("/u/detail",function(data){
            $("#totalscore").html(data.totalscore);
            $("#uname").val(data.nickname);
            $("#uheadimg").attr("src",data.headimg);
        })
    }
})



function stopPPG(e,url){
	if (e && e.stopPropagation) {//非IE浏览器
		e.stopPropagation();
	}
	else {//IE浏览器
		window.event.cancelBubble = true;
	}
	console.log(url)
	if(url){
	    location.href = url;
    }
}
var phoneCheck = false;
var nicknameCheck = false;
var passwordCheck = false;

function blur_phone(t){
    if(t.value.trim() == ""){
        login_input_error(t,"请填写手机号！");
        phoneCheck = false;
    }else{
        if(!checkPhone(t.value.trim())){
            login_input_error(t,"手机号格式有误！");
            phoneCheck = false;
        }else{
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("post","/u/exists",true);
            xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xmlhttp.onreadystatechange = function(){
                if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                    var jsonStr = JSON.parse(xmlhttp.responseText);
                    if(jsonStr.code == "0"){
                        reg_input_focus(t);
                        phoneCheck = true;
                        $("#phone_button").show();
                    }else{
                        login_input_error(t,"手机号已被使用！");
                        phoneCheck = false;
                    }
                }
            };
            xmlhttp.send("phone="+t.value);
        }
    }
}
var pcode;
var phoneNumber;
function getVCode(){
    if(phoneCheck){
        phoneNumber = $("#phone").val();
        $.post("/u/phonecode",{phone:$("#phone").val()},function(data){
            if(data.code == 0){
                $("#VCode").show();
                pcode = data.phone_code;
                $("#phone_button").attr("onclick","");
                countDown();
                countDonwTiming = setInterval(countDown,1000);
            }else{
                swal("验证码错误", "短信发送失败~！请您稍后再试！", "error");
            }
        },"json")
    }else{
        swal("验证码错误", "请您补全手机信息，确保正确后继续~", "error");
    }
}
var countDonwTiming;
var countDonwSum = 60;
function countDown(){
    if(countDonwSum == -1){
        clearInterval(countDonwTiming);
        countDonwSum = 60;
        $("#phone_button").html("发送验证码");
        $("#phone_button").attr("onclick","getVCode()");
        return "";
    }
    $("#phone_button").html(countDonwSum+"秒");
    countDonwSum--;
}
function checkPhone(phone){
    if(!(/^1[34578]\d{9}$/.test(phone))){
        return false;
    }
    return true
}
function blur_nickname(t){
    if(t.value.trim() == ""){
        login_input_error(t,"请输入昵称！");
        nicknameCheck = false;
    }else if(check_name(t.value.trim()) == "char"){
        login_input_error(t,"包含非法字符！请输入中文、数字、字母、下划线！");
        nicknameCheck = false;
    }else if(check_name(t.value.trim()) == "2-10"){
        login_input_error(t,"昵称长度为2-10位！");
        nicknameCheck = false;
    }else{
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("post","/u/exists",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status==200){
                var jsonStr = JSON.parse(xmlhttp.responseText);
                if(jsonStr.code == "0"){
                    reg_input_focus(t);
                    nicknameCheck = true;
                }else{
                    login_input_error(t,"昵称已被使用！");
                    nicknameCheck = false;
                }
            }
        };
        xmlhttp.send("nickname="+t.value);
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
        login_input_error(t,"密码不能为空！");
        passwordCheck = false;
    }else{
        reg_input_focus(t);
        passwordCheck = true;
    }
}
function check_name(str){
    var re1=/[a-zA-Z]|[0-9]|_/g;
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
            return '2-10';
        }
    }else{
        return 'char';
    }
}
function reg_submit(){
    var nickname = $("#nickname").val();
    var phone = $("#phone").val();
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
            // var jsonStr = JSON.parse(xmlhttp.responseText);
            // if(jsonStr.code == "0"){
            //     var hash = {
            //         'qq.com': 'http://mail.qq.com',
            //         'gmail.com': 'http://mail.google.com',
            //         'sina.com': 'http://mail.sina.com.cn',
            //         '163.com': 'http://mail.163.com',
            //         '126.com': 'http://mail.126.com',
            //         'yeah.net': 'http://www.yeah.net/',
            //         'sohu.com': 'http://mail.sohu.com/',
            //         'tom.com': 'http://mail.tom.com/',
            //         'sogou.com': 'http://mail.sogou.com/',
            //         '139.com': 'http://mail.10086.cn/',
            //         'hotmail.com': 'http://www.hotmail.com',
            //         'live.com': 'http://login.live.com/',
            //         'live.cn': 'http://login.live.cn/',
            //         'live.com.cn': 'http://login.live.com.cn',
            //         '189.com': 'http://webmail16.189.cn/webmail/',
            //         'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
            //         'yahoo.cn': 'http://mail.cn.yahoo.com/',
            //         'eyou.com': 'http://www.eyou.com/',
            //         '21cn.com': 'http://mail.21cn.com/',
            //         '188.com': 'http://www.188.com/',
            //         'foxmail.com': 'http://www.foxmail.com',
            //         'outlook.com': 'http://www.outlook.com'
            //     }
            //     swal({
            //         title: "注册成功！",
            //         text: "激活邮件已经发送至您的邮箱，请前去激活！",
            //         type: "success",
            //         showCancelButton: true,
            //         confirmButtonColor: "#DD6B55",
            //         confirmButtonText: "邮箱激活",
            //         cancelButtonColor: "#4DB6AC",
            //         cancelButtonText: "完成",
            //         closeOnConfirm: false
            //     },
            //     function(){
            //         // 点击登录邮箱
            //         var _mail = $("#email").val().split('@')[1];    //获取邮箱域
            //         for (var j in hash){
            //             if(j == _mail){
            //                 //跳转邮箱链接
            //                 window.open(hash[_mail],"_self");
            //             }
            //         }
            //     });
            // }else{
            //     swal("错误！", "注册失败！", "warning");
            // }
            var jsonStr = JSON.parse(xmlhttp.responseText);
            if(jsonStr.code == "0"){
                swal({
                    title: "注册成功！",
                    text: "恭喜您成功注册智量酷，请开始您的IT之旅吧~",
                    type: "success",
                    showCancelButton: true,
                    // confirmButtonColor: "#DD6B55",
                    confirmButtonColor: "#4DB6AC",
                    confirmButtonText: "GO~",
                    showCancelButton: false,
                    // cancelButtonColor: "#4DB6AC",
                    // cancelButtonText: "完成",
                    closeOnConfirm: false
                },
                function(){
                    window.location.reload(true);
                });
            }else{
                swal("错误！", "注册失败！", "warning");
            }
        }
    };
    var str = "nickname="+nickname+"&" +
            "phone="+phone+"&" +
            "password="+password+"&" +
            "program_exp="+program_exp+"&" +
            "into_it="+into_it+"&" +
            "learn_habit="+learn_habit+"&" +
            "comp_use_time_day="+comp_use_time_day+"&" +
            "sex="+sex;
    xmlhttp.send(str);
}
function login(){
    var phone = $("#phone").val().trim();
    var password = $("#password").val().trim();
    login_input_focus($("#phone"));
    login_input_focus($("#password"));
    if(phone != ""){
        if(password != ""){
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
                        login_input_error($("#phone"),jsonStr.msg);
                    }else if (jsonStr.code = "3"){
                        login_input_error($("#password"),jsonStr.msg);
                    }
                }
            };
            var str = "phone="+phone+"&" +
                    "password="+password;
            xmlhttp.send(str);
        }else {
            login_input_error($("#password"),"请输入密码！");
        }
    }else{
        login_input_error($("#phone"),"请输入登陆手机号！");
    }
}
function login_enter(e){
    if(e.keyCode == 13){
        login();
    }
}

function register_show(){
    modal_left.style.width = "39%";
    modal_right.style.width = "61%";
    var xmlhttp2 = new XMLHttpRequest();
    xmlhttp2.open("get","/static/reg_left.html",true);
    xmlhttp2.onreadystatechange = function(){
        if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
            modal_left.innerHTML = xmlhttp2.responseText;
            var xmlhttp3 = new XMLHttpRequest();
            xmlhttp3.open("get","/static/reg_right.html",true);
            xmlhttp3.onreadystatechange = function(){
                if(xmlhttp3.readyState == 4 && xmlhttp3.status==200){
                    modal_right.innerHTML = xmlhttp3.responseText;
                    modal_left.style.animation = "modal_animation 0.8s";
                    modal_right.style.animation = "modal_animation 0.9s";
                    login_reg_svg.style.animation = "login_svg_animation 1s";
                    modal_left.style.animationFillMode = "forwards";
                    modal_right.style.animationFillMode = "forwards";
                    login_reg_svg.style.animationFillMode = "forwards";
                    $(':input').labelauty();
                }
            };
            xmlhttp3.send(null);
        }
    };
    xmlhttp2.send(null);
}
function login_show(){
    modal_left.style.width = "60%";
    modal_right.style.width = "40%";
    var xmlhttp2 = new XMLHttpRequest();
    xmlhttp2.open("get","/static/login_left.html",true);
    xmlhttp2.onreadystatechange = function(){
        if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
            modal_left.innerHTML = xmlhttp2.responseText;
            var xmlhttp3 = new XMLHttpRequest();
            xmlhttp3.open("get","/static/login_right.html",true);
            xmlhttp3.onreadystatechange = function(){
                if(xmlhttp3.readyState == 4 && xmlhttp3.status==200){
                    modal_right.innerHTML = xmlhttp3.responseText;
                    modal_left.style.animation = "modal_animation 0.8s";
                    modal_right.style.animation = "modal_animation 0.9s";
                    login_reg_svg.style.animation = "login_svg_animation 1s";
                    modal_left.style.animationFillMode = "forwards";
                    modal_right.style.animationFillMode = "forwards";
                    login_reg_svg.style.animationFillMode = "forwards";
                    $("#phone").focus();
                }
            };
            xmlhttp3.send(null);
        }
    };
    xmlhttp2.send(null);
}

function continue_animation(){
    if(phoneCheck&&nicknameCheck&&passwordCheck){
        if(pcode == MD5($("#VCode").val())){
            if(phoneNumber == $("#phone").val()){
                reg_right_div.style.animation = "continue_animation 0.8s";
                reg_right_div_2.style.animation = "continue_animation 0.8s";
                reg_right_div.style.animationFillMode = "forwards";
                reg_right_div_2.style.animationFillMode = "forwards";
                modal_left_h2_1.className = "";
                modal_left_h2_2.className = "modal_left_shadow";
                login_reg_svg.style.animation = "login_svg_close_animation 0.6s";
            }else{
                swal("注册信息", "验证码与手机号不匹配，请您核对后再次输入！", "error");
            }
        }else{
            swal("注册信息", "验证码错误，请您核对后再次输入！", "error");
        }
    }else{
        swal("注册信息", "请您补全所有必填信息，确保格式正确后继续！", "error");
    }
}
function change_reg(){
    login_right_div.style.opacity = 0;
    login_left_div_div.style.opacity = 0;
    setTimeout(function(){
        var xmlhttp2 = new XMLHttpRequest();
        xmlhttp2.open("get","/static/reg_left.html",true);
        xmlhttp2.onreadystatechange = function(){
            if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
                modal_left.innerHTML = xmlhttp2.responseText;
                login_reg_svg.style.animation = "change_login_svg_animation_2 0.4s";
                login_reg_svg.style.animationFillMode = "forwards";
                reg_left_div_div.style.animation = "show_modal_right_animation 0.4s";
                var xmlhttp3 = new XMLHttpRequest();
                xmlhttp3.open("get","/static/reg_right.html",true);
                xmlhttp3.onreadystatechange = function(){
                    if(xmlhttp3.readyState == 4 && xmlhttp3.status==200){
                        modal_right.innerHTML = xmlhttp3.responseText;
                        reg_right_div.style.animation = "show_modal_right_animation 0.4s";
                        reg_right_div_2.style.animation = "show_modal_right_animation 0.4s";
                        $(':input').labelauty();
                    }
                };
                xmlhttp3.send(null);
            }
        };
        xmlhttp2.send(null);
    },400);
    modal_left.style.animation = "change_reg_modal_left_animation 0.8s";
    modal_right.style.animation = "change_reg_modal_right_animation 0.8s";
    modal_left.style.animationFillMode = "forwards";
    modal_right.style.animationFillMode = "forwards";
    setTimeout(function(){
        login_reg_img.src = "/static/svg/loginSVG.svg";
    },800)
    login_reg_svg.style.animation = "change_reg_svg_animation_1 0.8s";
    login_reg_svg.style.animationFillMode = "forwards";
}
function change_login(){
    reg_right_div.style.opacity = 0;
    reg_right_div_2.style.opacity = 0;
    reg_left_div_div.style.opacity = 0;
    setTimeout(function(){
        var xmlhttp2 = new XMLHttpRequest();
        xmlhttp2.open("get","/static/login_left.html",true);
        xmlhttp2.onreadystatechange = function(){
            if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
                modal_left.innerHTML = xmlhttp2.responseText;
                login_reg_svg.style.animation = "change_reg_svg_animation_2 0.4s";
                login_reg_svg.style.animationFillMode = "forwards";
                login_left_div_div.style.animation = "show_modal_right_animation 0.4s";
                var xmlhttp3 = new XMLHttpRequest();
                xmlhttp3.open("get","/static/login_right.html",true);
                xmlhttp3.onreadystatechange = function(){
                    if(xmlhttp3.readyState == 4 && xmlhttp3.status==200){
                        modal_right.innerHTML = xmlhttp3.responseText;
                        login_right_div.style.animation = "show_modal_right_animation 0.4s";
                        $(':input').labelauty();
                    }
                };
                xmlhttp3.send(null);
            }
        };
        xmlhttp2.send(null);
    },400);
    modal_left.style.animation = "change_login_modal_left_animation 0.8s";
    modal_right.style.animation = "change_login_modal_right_animation 0.8s";
    modal_left.style.animationFillMode = "forwards";
    modal_right.style.animationFillMode = "forwards";
    setTimeout(function(){
        login_reg_img.src = "/static/svg/regSVG.svg";
    },800)
    login_reg_svg.style.animation = "change_login_svg_animation_1 0.8s";
    login_reg_svg.style.animationFillMode = "forwards";
}

function login_input_error(t,message){
    $(t).css("border","2px solid rgb(214,96,97)");
    $(t).parent().find("span").html(message);
    $(t).parent().find("span").slideDown();
}
function login_input_focus(t){
    $(t).css("border","2px solid transparent");
    $(t).parent().find("span").slideUp();
}
function reg_input_focus(t){
    $(t).css("border","2px solid #ECEFF1");
    $(t).parent().find("span").slideUp();
}
