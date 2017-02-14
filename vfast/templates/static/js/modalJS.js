function register_show(){
    modal_left.style.width = "39%";
    modal_right.style.width = "61%";
    var xmlhttp2 = new XMLHttpRequest();
    xmlhttp2.open("get","../static/reg_left.html",true);
    xmlhttp2.onreadystatechange = function(){
        if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
            modal_left.innerHTML = xmlhttp2.responseText;
            var xmlhttp3 = new XMLHttpRequest();
            xmlhttp3.open("get","../static/reg_right.html",true);
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
    console.log(111);
    modal_left.style.width = "60%";
    modal_right.style.width = "40%";
    var xmlhttp2 = new XMLHttpRequest();
    xmlhttp2.open("get","../static/login_left.html",true);
    xmlhttp2.onreadystatechange = function(){
        if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
            modal_left.innerHTML = xmlhttp2.responseText;
            var xmlhttp3 = new XMLHttpRequest();
            xmlhttp3.open("get","../static/login_right.html",true);
            xmlhttp3.onreadystatechange = function(){
                if(xmlhttp3.readyState == 4 && xmlhttp3.status==200){
                    modal_right.innerHTML = xmlhttp3.responseText;
                    modal_left.style.animation = "modal_animation 0.8s";
                    modal_right.style.animation = "modal_animation 0.9s";
                    login_reg_svg.style.animation = "login_svg_animation 1s";
                    modal_left.style.animationFillMode = "forwards";
                    modal_right.style.animationFillMode = "forwards";
                    login_reg_svg.style.animationFillMode = "forwards";
                }
            };
            xmlhttp3.send(null);
        }
    };
    xmlhttp2.send(null);
}

function continue_animation(){
    if(usernameCheck&&emailCheck&&passwordCheck){
        reg_right_div.style.animation = "continue_animation 0.8s";
        reg_right_div_2.style.animation = "continue_animation 0.8s";
        reg_right_div.style.animationFillMode = "forwards";
        reg_right_div_2.style.animationFillMode = "forwards";
        modal_left_h2_1.className = "";
        modal_left_h2_2.className = "modal_left_shadow";
        login_reg_svg.style.animation = "login_svg_close_animation 0.6s";
    }else{
        swal("注册错误", "请您补全所有必填信息，确保格式正确后继续~", "error");
    }
}
function change_reg(){
    login_right_div.style.opacity = 0;
    login_left_div_div.style.opacity = 0;
    setTimeout(function(){
        var xmlhttp2 = new XMLHttpRequest();
        xmlhttp2.open("get","../static/reg_left.html",true);
        xmlhttp2.onreadystatechange = function(){
            if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
                modal_left.innerHTML = xmlhttp2.responseText;
                login_reg_svg.style.animation = "change_login_svg_animation_2 0.4s";
                login_reg_svg.style.animationFillMode = "forwards";
                reg_left_div_div.style.animation = "show_modal_right_animation 0.4s";
                var xmlhttp3 = new XMLHttpRequest();
                xmlhttp3.open("get","../static/reg_right.html",true);
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
        login_reg_img.src = "../static/svg/loginSVG.svg";
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
        xmlhttp2.open("get","../static/login_left.html",true);
        xmlhttp2.onreadystatechange = function(){
            if(xmlhttp2.readyState == 4 && xmlhttp2.status==200){
                modal_left.innerHTML = xmlhttp2.responseText;
                login_reg_svg.style.animation = "change_reg_svg_animation_2 0.4s";
                login_reg_svg.style.animationFillMode = "forwards";
                login_left_div_div.style.animation = "show_modal_right_animation 0.4s";
                var xmlhttp3 = new XMLHttpRequest();
                xmlhttp3.open("get","../static/login_right.html",true);
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
        login_reg_img.src = "../static/svg/regSVG.svg";
    },800)
    login_reg_svg.style.animation = "change_login_svg_animation_1 0.8s";
    login_reg_svg.style.animationFillMode = "forwards";
}
