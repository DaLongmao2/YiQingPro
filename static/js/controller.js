// 发送ajax请求

function get_time() {
    $.ajax({
        url: '/get_time/',
        type: 'post',
        success: function (data) {
            $("#time").html(data)
        },
        error: function () {
            // TODO: ERROR
        }
    })
}


function get_center1() {
    $.ajax({
        url: '/get_center1/',
        type: 'post',
        success: function (data) {
            $(".num h1").eq(0).html(data['confirm'])
            $(".num h1").eq(1).html(data['suspect'])
            $(".num h1").eq(2).html(data['heal'])
            $(".num h1").eq(3).html(data['dead'])
        },
        error: {}
    })
}


function get_center2(){
    $.ajax({
        url: /get_center2/,
        type:'post',
        success:function(data){
            console.log(data);
            ec_center_option.series[0].data = data.data
            ec_center.setOption(ec_center_option)
            console.log(data['data']);
        },
        error:function(){}
    })
}

function get_left1(){
    $.ajax({
        url: '/get_left1/',
        type:'post',
        success: function (data){
            ec_left1_Option.xAxis[0].data=data['day']
            ec_left1_Option.series[0].data=data['confirm']
            ec_left1_Option.series[1].data=data['suspect']
            ec_left1_Option.series[2].data=data['heal']
            ec_left1_Option.series[2].data=data['dead']
            ec_left1.setOption(ec_left1_Option)
        },
        error:function (){

        }
    })
}

function get_left2() {
    $.ajax({
        url:"/get_left2/",
        success: function(data) {
			ec_left2_Option.xAxis[0].data=data.day
            ec_left2_Option.series[0].data=data.confirm_add
            ec_left2_Option.series[1].data=data.suspect_add
            ec_left2.setOption(ec_left2_Option)
		},
		error: function(xhr, type, errorThrown) {

		}
    })
}


function get_right1() {
    $.ajax({
        url: "/get_right1/",
        type:'post',
        success: function (data) {
            ec_right1_option.xAxis.data=data.city;
            ec_right1_option.series[0].data=data.confirm;
            ec_right1.setOption(ec_right1_option);
        }
    })
}


// 实时词云
function get_right2() {
    $.ajax({
        url: "/get_right2/",
        success: function (data) {
            ec_right2_option.series[0].data=data.kws;
            ec_right2.setOption(ec_right2_option);
        }
    })
}

function update() {
    $.ajax({
        url: "/update/",
        type:'post',
        success: function (data) {
            console.log('更新完成');
        }
    })
}
setInterval(get_time, 1000)
setInterval(get_center1, 1000)
setInterval(get_center2, 1000)
setInterval(get_left1, 1000)
setInterval(get_left2, 1000)
setInterval(get_right1, 1000)
setInterval(get_right2, 1000)
