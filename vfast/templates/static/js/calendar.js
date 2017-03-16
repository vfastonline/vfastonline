var CalendarHandler = {
    currentYear: 0,
    currentMonth: 0,
    isRunning: false,
    showYearStart:2009,
    tag:0,
    initialize: function() {
        $calendarItem = this.CreateCalendar(0, 0, 0);
        $("#Container").append($calendarItem);

        $("#context").css("height", $("#CalendarMain").height() - 65 + "px");
        $("#center").css("height", $("#context").height() - 38 + "px");
        $("#selectYearDiv").css("height", $("#context").height() - 38 + "px").css("width", $("#context").width() + "px");
        $("#selectMonthDiv").css("height", $("#context").height() - 38 + "px").css("width", $("#context").width() + "px");
        $("#centerCalendarMain").css("height", $("#context").height() - 38 + "px").css("width", $("#context").width() + "px");

        $calendarItem.css("height", $("#context").height() - 38 + "px"); //.css("visibility","hidden");
        $("#Container").css("height", "0px").css("width", "0px").css("margin-left", $("#context").width() / 2 + "px").css("margin-top", ($("#context").height() - 30) / 2 + "px");
        $("#Container").animate({
            width: $("#context").width() + "px",
            height: ($("#context").height() - 38) * 2 + "px",
            marginLeft: "0px",
            marginTop: "0px"
        }, 300, function() {
            $calendarItem.css("visibility", "visible");
        });
        $(".dayItem").css("width", $("#context").width() + "px");
        var itemPaddintTop = $(".dayItem").height() / 6;
        $(".item").css({
            "width": $(".week").width() / 7 -24 + "px",
            "line-height": itemPaddintTop-3 + "px",
            "height": itemPaddintTop-3 + "px",
            "margin":"3px 12px 0px 12px"
        });
        $(".week>h3").css("width", $(".week").width() / 7 + "px");
    },
    IsRuiYear: function(aDate) {
        return (0 == aDate % 4 && (aDate % 100 != 0 || aDate % 400 == 0));
    },
    CalculateWeek: function(y, m, d) {
        var arr = "7123456".split("");
        with(document.all) {
            var vYear = parseInt(y, 10);
            var vMonth = parseInt(m, 10);
            var vDay = parseInt(d, 10);
        }
        var week =arr[new Date(y,m-1,vDay).getDay()];
        return week;
    },
    CalculateMonthDays: function(m, y) {
        var mDay = 0;
        if (m == 0 || m == 1 || m == 3 || m == 5 || m == 7 || m == 8 || m == 10 || m == 12) {
            mDay = 31;
        } else {
            if (m == 2) {
                //判断是否为芮年
                var isRn = this.IsRuiYear(y);
                if (isRn == true) {
                    mDay = 29;
                } else {
                    mDay = 28;
                }
            } else {
                mDay = 30;
            }
        }
        return mDay;
    },
    CreateCalendar: function(y, m, d) {
        $dayItem = $("<div class=\"dayItem\"></div>");
        //获取当前月份的天数
        var nowDate = new Date();
        if(y==nowDate.getFullYear()&&m==nowDate.getMonth()+1||(y==0&&m==0))
        $(".currentDay").hide();
        var nowYear = y == 0 ? nowDate.getFullYear() : y;
        this.currentYear = nowYear;
        var nowMonth = m == 0 ? nowDate.getMonth() + 1 : m;
        this.currentMonth = nowMonth;
        var nowDay = d == 0 ? nowDate.getDate() : d;
        $(".selectYear").html(nowYear + "年");
        $(".selectMonth").html(nowMonth + "月");
        var nowDaysNub = this.CalculateMonthDays(nowMonth, nowYear);
        //获取当月第一天是星期几
        //var weekDate = new Date(nowYear+"-"+nowMonth+"-"+1);
        //alert(weekDate.getDay());
        var nowWeek = parseInt(this.CalculateWeek(nowYear, nowMonth, 1));
        //nowWeek=weekDate.getDay()==0?7:weekDate.getDay();
        //var nowWeek=weekDate.getDay();
        //获取上个月的天数
        var lastMonthDaysNub = this.CalculateMonthDays((nowMonth - 1), nowYear);

        if (nowWeek != 0) {
            //生成上月剩下的日期
            for (var i = (lastMonthDaysNub - (nowWeek - 1)); i < lastMonthDaysNub; i++) {
                $dayItem.append("<div class=\"item lastItem\"><a>" + (i + 1) + "</a></div>");
            }
        }

        //生成当月的日期
        for (var i = 0; i < nowDaysNub; i++) {
            if (i == (nowDay - 1)) $dayItem.append("<div class=\"item currentItem\"><a>" + (i + 1) + "</a></div>");
            else $dayItem.append("<div class=\"item\"><a>" + (i + 1) + "</a></div>");
        }

        //获取总共已经生成的天数
        var hasCreateDaysNub = nowWeek + nowDaysNub;
        //如果小于42，往下个月推算
        if (hasCreateDaysNub < 42) {
            for (var i = 0; i <= (42 - hasCreateDaysNub); i++) {
                $dayItem.append("<div class=\"item lastItem\"><a>" + (i + 1) + "</a></div>");
            }
        }

        return $dayItem;
    },
    CSS: function() {
        var itemPaddintTop = $(".dayItem").height() / 6;
        $(".item").css({
            "width": $(".week").width() / 7 -24 + "px",
            "line-height": itemPaddintTop-3 + "px",
            "height": itemPaddintTop-3 + "px",
            "margin":"3px 12px 0px 12px"
        });
    },
    CalculateNextMonthDays: function() {
        if (this.isRunning == false) {
            $(".currentDay").show();
            var m = this.currentMonth == 12 ? 1 : this.currentMonth + 1;
            var y = this.currentMonth == 12 ? (this.currentYear + 1) : this.currentYear;
            var d = 0;
            var nowDate = new Date();
            if (y == nowDate.getFullYear() && m == nowDate.getMonth() + 1) d = nowDate.getDate();
            else d = 1;
            $calendarItem = this.CreateCalendar(y, m, d);
            $("#Container").append($calendarItem);

            this.CSS();
            this.isRunning = true;
            $($("#Container").find(".dayItem")[0]).animate({
                height: "0px"
            }, 300, function() {
                $(this).remove();
                CalendarHandler.isRunning = false;
            });
        }
        getScore();
    },
    CalculateLastMonthDays: function() {
        if (this.isRunning == false) {
            $(".currentDay").show();
            var nowDate = new Date();
            var m = this.currentMonth == 1 ? 12 : this.currentMonth - 1;
            var y = this.currentMonth == 1 ? (this.currentYear - 1) : this.currentYear;
            var d = 0;

            if (y == nowDate.getFullYear() && m == nowDate.getMonth() + 1) d = nowDate.getDate();
            else d = 1;
            $calendarItem = this.CreateCalendar(y, m, d);
            $("#Container").append($calendarItem);
            var itemPaddintTop = $(".dayItem").height() / 6;
            this.CSS();
            this.isRunning = true;
            $($("#Container").find(".dayItem")[0]).animate({
                height: "0px"
            }, 300, function() {
                $(this).remove();
                CalendarHandler.isRunning = false;
            });
        }
        getScore();
    },
    CreateCurrentCalendar: function() {
        if (this.isRunning == false) {
            $(".currentDay").hide();
            $calendarItem = this.CreateCalendar(0, 0, 0);
            $("#Container").append($calendarItem);
            this.isRunning = true;
            $($("#Container").find(".dayItem")[0]).animate({
                height: "0px"
            }, 300, function() {
                $(this).remove();
                CalendarHandler.isRunning = false;
            });
            this.CSS();
            $("#centerMain").animate({
                marginLeft: -$("#center").width() + "px"
            }, 500);
        }
    }
}