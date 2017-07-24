$(function(){
	$("body").css("opacity","1");
	$(".slideDIV").slideUp(350);
	if($("#uid").val() != ""){
        $.getJSON("/u/detail",function(data){
            $("#totalscore").html(data.totalscore);
            $("#uname").val(data.nickname);
            $("#uheadimg").attr("src",data.headimg);
        })

        $.get("/info/getinfo",function(data){
            if(data.length > 0){
                $("#remindSum").html(data.length);
                $("#remindSum").show();
            }
            for(var i = 0 ; i < data.length ; i++){
                var infoStr = "";
                infoStr += '<div id="'+data[i].inform_id+'" class="remind_content clearfix" onclick="remind_go(this,\''+data[i].url+'\')">';
                infoStr += '<div>';
                switch (data[i].type_name){
                    case "新课程":
                        infoStr += '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="25" viewBox="0 0 19 25"><path fill="'+data[i].color+'" fill-rule="evenodd" d="M688.630495,304.229528 L677.467922,298.476064 C675.939198,297.670391 672.924518,299.226811 672.058538,300.596326 C671.671965,301.208233 671.700211,301.650226 671.700211,301.90021 L671.837789,314.893891 C671.847204,315.169815 672.194606,315.541894 672.491638,315.724489 C673.110901,316.104446 682.488674,321.95887 682.75521,322.124693 C682.89814,322.213438 683.066762,322.255161 683.233574,322.255161 C683.375488,322.255161 683.517897,322.223869 683.646855,322.159801 C683.928653,322.021455 684.104385,321.752394 684.104385,321.460166 L684.104385,307.812388 C684.104385,307.528559 683.938562,307.265592 683.668732,307.123677 L673.522645,301.460248 C673.63733,301.237467 674.08926,300.76569 674.918348,300.330806 C675.7927,299.873276 676.447071,300.045962 676.597358,300.103963 C676.597358,300.103963 686.334473,305.314968 686.632548,305.469592 C686.929333,305.624462 686.934686,305.64763 686.934686,305.912628 L686.934686,318.863077 C686.934686,319.509048 687.590567,319.773552 688.072006,319.773552 C688.552923,319.773552 689.065873,319.302298 689.065873,318.863077 L689.065873,304.918486 C689.066148,304.63441 688.899309,304.371717 688.630495,304.229528 L688.630495,304.229528 Z" transform="translate(-671 -298)"/></svg>';
                        break;
                    case "新路线":
                        infoStr += '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="18" viewBox="0 0 19 18"><path fill="'+data[i].color+'" d="M675.582813,628 C677.792813,628 679.582813,629.79 679.582813,632 C679.582813,633.86 678.312813,635.43 676.582813,635.87 L676.582813,638.13 C676.952813,638.22 677.302813,638.37 677.622813,638.56 L682.142813,634.04 C681.782813,633.44 681.582813,632.75 681.582813,632 C681.582813,629.79 683.372813,628 685.582813,628 C687.792813,628 689.582813,629.79 689.582813,632 C689.582813,634.21 687.792813,636 685.582813,636 C684.842813,636 684.152813,635.8 683.582813,635.45 L679.032813,640 C679.382813,640.57 679.582813,641.26 679.582813,642 C679.582813,644.21 677.792813,646 675.582813,646 C673.372813,646 671.582813,644.21 671.582813,642 C671.582813,640.14 672.852813,638.57 674.582813,638.13 L674.582813,635.87 C672.852813,635.43 671.582813,633.86 671.582813,632 C671.582813,629.79 673.372813,628 675.582813,628 L675.582813,628 Z M685.582813,638 C687.792813,638 689.582813,639.79 689.582813,642 C689.582813,644.21 687.792813,646 685.582813,646 C683.372813,646 681.582813,644.21 681.582813,642 C681.582813,639.79 683.372813,638 685.582813,638 L685.582813,638 Z M685.582813,640 C684.482813,640 683.582813,640.9 683.582813,642 C683.582813,643.1 684.482813,644 685.582813,644 C686.682813,644 687.582813,643.1 687.582813,642 C687.582813,640.9 686.682813,640 685.582813,640 Z" transform="translate(-671 -628)"/></svg>';
                        break;
                    case "新事项":
                        infoStr += '<svg xmlns="http://www.w3.org/2000/svg" width="21" height="17" viewBox="0 0 21 17"><path fill="'+data[i].color+'" d="M688.382813,547.28701 C689.492813,547.28701 690.382813,548.17701 690.382813,549.28701 L690.382813,561.28701 C690.382813,562.39701 689.492813,563.28701 688.382813,563.28701 L672.382813,563.28701 C671.272813,563.28701 670.382813,562.39701 670.382813,561.28701 L670.382813,549.28701 C670.382813,548.17701 671.272813,547.28701 672.382813,547.28701 L688.382813,547.28701 L688.382813,547.28701 Z M676.882813,558.28701 L676.882813,552.28701 L675.632813,552.28701 L675.632813,555.78701 L673.132813,552.28701 L671.882813,552.28701 L671.882813,558.28701 L673.132813,558.28701 L673.132813,554.78701 L675.682813,558.28701 L676.882813,558.28701 L676.882813,558.28701 Z M681.882813,553.54701 L681.882813,552.28701 L677.882813,552.28701 L677.882813,558.28701 L681.882813,558.28701 L681.882813,557.03701 L679.382813,557.03701 L679.382813,555.92701 L681.882813,555.92701 L681.882813,554.66701 L679.382813,554.66701 L679.382813,553.54701 L681.882813,553.54701 L681.882813,553.54701 Z M688.882813,557.28701 L688.882813,552.28701 L687.632813,552.28701 L687.632813,556.78701 L686.512813,556.78701 L686.512813,553.28701 L685.262813,553.28701 L685.262813,556.78701 L684.132813,556.78701 L684.132813,552.28701 L682.882813,552.28701 L682.882813,557.28701 C682.882813,557.83701 683.332813,558.28701 683.882813,558.28701 L687.882813,558.28701 C688.432813,558.28701 688.882813,557.83701 688.882813,557.28701 Z" transform="translate(-670 -547)"/></svg>';
                        break;
                    case "新动态":
                        infoStr += '<svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21"><path fill="'+data[i].color+'" d="M681.255874,717.228101 L673.065874,721.038101 L676.875874,712.848101 L685.065874,709.038101 L681.255874,717.228101 Z M679.065874,705.038101 C673.545874,705.038101 669.065874,709.518101 669.065874,715.038101 C669.065874,720.558101 673.545874,725.038101 679.065874,725.038101 C684.585874,725.038101 689.065874,720.558101 689.065874,715.038101 C689.065874,709.518101 684.585874,705.038101 679.065874,705.038101 L679.065874,705.038101 Z M679.065874,713.938101 C678.455874,713.938101 677.965874,714.428101 677.965874,715.038101 C677.965874,715.648101 678.455874,716.138101 679.065874,716.138101 C679.675874,716.138101 680.165874,715.648101 680.165874,715.038101 C680.165874,714.428101 679.675874,713.938101 679.065874,713.938101 Z" transform="translate(-669 -705)"/></svg>';
                        break;
                    case "问题回复":
                        infoStr += '<svg xmlns="http://www.w3.org/2000/svg" width="23" height="19" viewBox="0 0 23 19"><path fill="'+data[i].color+'" d="M677.938368,470.848818 L677.938368,465.959929 L669.382813,474.515484 L677.938368,483.07104 L677.938368,478.059929 C684.049479,478.059929 688.327257,480.015484 691.382813,484.293262 C690.160591,478.182151 686.493924,472.07104 677.938368,470.848818 Z" transform="translate(-669 -466)"/></svg>';
                        break;
                }
                infoStr += '</div>';
                infoStr += '<div>';
                infoStr += '<h5>'+data[i].type_name+'</h5>';
                infoStr += '<p>'+data[i].desc+'</p>';
                infoStr += '<span>'+data[i].pubtime+'</span>';
                infoStr += '</div>';
                infoStr += '<hr/>';
                infoStr += '</div>';
                $("#remind_div").prepend(infoStr);
            }
        },'json')
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
    $("#reg_submit").removeAttr("onclick");
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
            var jsonStr = JSON.parse(xmlhttp.responseText);
            if(jsonStr.code == "0"){
                swal({
                    title: "注册成功！",
                    text: "恭喜您成功注册智量酷，请开始您的IT之旅吧~",
                    type: "success",
                    //showCancelButton: true,
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
                $("#reg_submit").attr("onclick","reg_submit()");
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
function remind_show(){
    $("#myModal_remind .modal-dialog").css("animation","remind_animation 0.35s");
}
function clear_remind(){
    $(".remind_content").css("animation","clear_remind_animation 0.4s");
    setTimeout(function(){
        $("#remind_div").html("");
        $("#remindSum").html("0");
        $("#remindSum").hide();
        $.get("/info/dall",function(){});
    },350);
}
function remind_go(t,url){
    $.get("/info/done?inform_id="+t.id,function(){});
    $(t).remove();
    location.href = url;
}
function showFeedback(){
    $("#feedback_dialog").addClass("animated fadeInUp");
}
function closeFeedback(){
    $("#myFeedback_info").click();
}
function showFeedbackSend(e,t){
    if($(t).val().trim() != "" ){
        $("#feedbackSendSvg").css("visibility","visible");
    }else{
        $("#feedbackSendSvg").css("visibility","hidden");
    }
}
$("#feedbackSendSvg").on("click",function(){
    $.post("/info/create_feedback",{"description":$("#feedback_text").val()},function(data){
        console.log(data);
        if(data.code == 0){
            swal("发送成功~", "感谢您的宝贵意见，我们将尽快给予您答复~谢谢！", "success");
            $("#myFeedback_info").click();
        }
    },"JSON")
})