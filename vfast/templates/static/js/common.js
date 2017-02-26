$(function(){
	$("body").css("opacity","1");
	$(".slideDIV").slideUp(350);
})

function stopPPG(e){
	if (e && e.stopPropagation) {//非IE浏览器
		e.stopPropagation();
	}
	else {//IE浏览器
		window.event.cancelBubble = true;
	}
}