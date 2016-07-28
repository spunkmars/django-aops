function get_dict_keys(dict){
    var v_list = [];
    for(var key in dict){
        v_list.push(key);
    }
    return v_list;
}


function get_dict_values(dict){
    var v_list = [];
    for(var key in dict){
        v_list.push(dict[key]);
    }
    return v_list;
}

//随机取数组中的数值。
function getArrayItems(arr, num) {
    //新建一个数组,将传入的数组复制过来,用于运算,而不要直接操作传入的数组;
    var temp_array = new Array();
    for (var index in arr) {
        temp_array.push(arr[index]);
    }
    //取出的数值项,保存在此数组
    var return_array = new Array();
    for (var i = 0; i<num; i++) {
        //判断如果数组还有可以取出的元素,以防下标越界
        if (temp_array.length>0) {
            //在数组中产生一个随机索引
            var arrIndex = Math.floor(Math.random()*temp_array.length);
            //将此随机索引的对应的数组元素值复制出来
            return_array[i] = temp_array[arrIndex];
            //然后删掉此索引的数组元素,这时候temp_array变为新的数组
            temp_array.splice(arrIndex, 1);
        } else {
            //数组中数据项取完后,退出循环,比如数组本来只有10项,但要求取出20项.
            break;
        }
    }
    return return_array;
}


function make_chart(chart_id, option){
    var chart = echarts.init(document.getElementById(chart_id)).setOption(option);
    return chart;
}


function get_mdc_option(title_name, data, color_list){

    var data_keys = get_dict_keys(data);
    var t_data = [];
    
    for (var i in data_keys){
        t_data.push({value:data[data_keys[i]], name:data_keys[i]});
        //alert(data_keys[i])
    }
    
    var option1 = {
        title : {
            text: title_name,
           // subtext: '纯属虚构',
            x:'center'
        },
    
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
    
        legend: {
            //orient : 'vertical',
            x : 'center',
            y : 'bottom',
            data:data_keys
    
        },
    
        /*
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {
                    show: true,
                    type: ['pie', 'funnel'],
                    option: {
                        funnel: {
                            x: '10%',
                            width: '50%',
                            funnelAlign: 'left',
                            max: 300000
                        }
                    }
                },
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        */
        calculable : true,
        series : [
            {
                name:title_name,
                type:'pie',
                itemStyle: {
                    normal: {
                        color: function(params) {
                            // build a color map as your need.
                            var colorList = color_list;
                            return colorList[params.dataIndex]
                        },
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{b}\n({c})'
                            //formatter: '{c}'
                        }
                    }
                },
                radius : '52%',
                center: ['50%', '52%'],
                data:t_data
            }
        ]
    };

    return option1
}

function get_mbc_option(s_title,data,color_list){

    var data_keys = get_dict_keys(data);
    var data_values = get_dict_values(data);
    var option2 = {
        title: {
            x: 'center',
            text: s_title,
            //subtext: 'Rainbow bar example',
            //link: 'http://echarts.baidu.com/doc/example.html'
        },
        tooltip: {
            trigger: 'item'
        },
        /*
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        */
        calculable: true,
        grid: {
            borderWidth: 0,
            y: 80,
            y2: 60
        },
        xAxis: [
            {
                type: 'category',
                show: false,
                data: data_keys
            }
        ],
        yAxis: [
            {
                type: 'value',
                show: false
            }
        ],
        series: [
            {
                name: s_title,
                type: 'bar',
                itemStyle: {
                    normal: {
                        color: function(params) {
                            // build a color map as your need.
                            var colorList = color_list
                            return colorList[params.dataIndex]
                        },
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{b}\n{c}'
                            //formatter: '{c}'
                        }
                    }
                },
                data: data_values,
    
                /*
                markPoint: {
                    tooltip: {
                        trigger: 'item',
                        backgroundColor: 'rgba(0,0,0,0)',
                        formatter: function(params){
                            return '<img src="'
                                    + params.data.symbol.replace('image://', '')
                                    + '"/>';
                        }
                    },
                    data: [
                        {xAxis:0, y: 350, name:'Line', symbolSize:20, symbol: 'image://../asset/ico/折线图.png'},
                        {xAxis:1, y: 350, name:'Bar', symbolSize:20, symbol: 'image://../asset/ico/柱状图.png'},
                        {xAxis:2, y: 350, name:'Scatter', symbolSize:20, symbol: 'image://../asset/ico/散点图.png'},
                        {xAxis:3, y: 350, name:'K', symbolSize:20, symbol: 'image://../asset/ico/K线图.png'},
                        {xAxis:4, y: 350, name:'Pie', symbolSize:20, symbol: 'image://../asset/ico/饼状图.png'},
                        {xAxis:5, y: 350, name:'Radar', symbolSize:20, symbol: 'image://../asset/ico/雷达图.png'},
                        {xAxis:6, y: 350, name:'Chord', symbolSize:20, symbol: 'image://../asset/ico/和弦图.png'},
                        {xAxis:7, y: 350, name:'Force', symbolSize:20, symbol: 'image://../asset/ico/力导向图.png'},
                        {xAxis:8, y: 350, name:'Map', symbolSize:20, symbol: 'image://../asset/ico/地图.png'},
                        {xAxis:9, y: 350, name:'Gauge', symbolSize:20, symbol: 'image://../asset/ico/仪表盘.png'},
                        {xAxis:10, y: 350, name:'Funnel', symbolSize:20, symbol: 'image://../asset/ico/漏斗图.png'},
                    ]
                }
    
                */
            }
        ]
    };
    return option2;
}



function get_ebc_option(s_title, data, s_type){

    var seriesArr = new Array();
    var legend_data = new Array();
    var series = data.series;
    //console.log(s_title)
    for(var i in series){
        legend_data.push(series[i].name);
        seriesArr.push({'name':series[i].name, 'type':'bar', 'stack':series[i].stack, 'itemStyle':{ normal: {label : {show: true, position: 'insideRight'}}}, 'data':series[i].data});
    }


    var category = {
            type : 'category',
            itemStyle : { normal: {label : {show: false, position: 'top',formatter: '{b} vv{c}'}}},
            data : data.x_category,
            axisLabel:{
                interval:0 //0：表示全部显示不间隔；auto:表示自动根据刻度个数和宽度自动设置间隔个数
            }
        }

    var value =  {
            type : 'value',
            splitArea : {show : false},
        }

    var xAxis;
    var yAxis;

    if (s_type != 'normal') {
        xAxis = category;
        yAxis = value;
    } else {
        xAxis = value;
        yAxis = category;
    }

    //console.log(seriesArr)
    var option2 = {
     title: {
        x: 'center',
       // y:'bottom',
        text: s_title,
        //subtext: 'Rainbow bar example',
        //link: 'http://echarts.baidu.com/doc/example.html'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        x: 'center',
        y:'bottom',
        data:legend_data
    },

    toolbox: {
        show : true,
        x: 'right',
        y:'center',
        orient : 'vertical',
        feature : {
            //mark : {show: true},
            dataView : {show: true, readOnly: true},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },


    calculable : true,
    xAxis : [ xAxis

    ],
    yAxis : [ yAxis


    ],
    series : seriesArr,
};

    return option2;

}



   // 渲染图表主题。
    var myChart = new Array();
    var curTheme;
    var defaultTheme = 'macarons';
    var theme_path = '/static/echarts/build/dist/theme/';



    function showloading(){
        for(var i in myChart){
            myChart[i].showLoading();
        }
    }


    function hideLoading(){
        for(var i in myChart){
            myChart[i].hideLoading();
        }
    }

    function refreshTheme(){
        //hideLoading();
        for(var i in myChart){
            myChart[i].setTheme(curTheme);
        }
    }



    color_list = [
                  '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                  '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                  '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
        ];

    //make_chart('morris-donut-chart01', get_mdc_option('物理主机', {'有效':100,'备用':20, '无效':5}, getArrayItems(color_list, 3)))
    //make_chart('morris-donut-chart02', get_mdc_option('网络设备', {'有效':100,'备用':20, '无效':2}, getArrayItems(color_list, 3)))
    //make_chart('morris-donut-chart03', get_mdc_option('主机', {'在线':200,'备用':20, '无效':0},  getArrayItems(color_list, 3)))
    //make_chart('morris-donut-chart04', get_mdc_option('机柜', {'有效':8,'备用':2, '无效':0}, getArrayItems(color_list, 3)))


    //mbc_data1 = {'物理主机':100, '主机':300, '网络设备':20, '机柜':13};
    //make_chart('morris-bar-chart01', get_mbc_option('资产概况', mbc_data1, color_list))

    //mbc_data2 ={'tomcat':50, 'mysql':20, 'postgresql':5, 'nginx':30, 'apache':2, 'redis':100, 'memcached':2, 'php':2, 'rabbitmq':2, 'logstash':6, 'zabbix':2};
    //make_chart('morris-bar-chart02', get_mbc_option('应用概况', mbc_data2, color_list))



var update_time = 3000;
var getdata;


function send_info(){
    var getdata;
    var send_data = {'data':'load...'};
    getdata = {
        poll: function(){
            $.ajax({url: "/dashboard_ajax/",
                    //type: "GET",
                    type: "POST",
                    data: send_data,
                    dataType: 'json',
                    success: getdata.onSuccess,
                    error: getdata.onError});
        },
	    onSuccess: function(data, dataStatus){
	       //alert("A :  " + data.a)
           //console.log("E :  " + data.e)
           var mdc = data.mdc;
           var mbc = data.mbc;
           var ebc = data.ebc;

           for(var i in mdc){
               myChart.push(make_chart(mdc[i].chart_id, get_mdc_option(mdc[i].s_title, mdc[i].data, getArrayItems(color_list, 3))));
           }

           for(var i in mbc){
               myChart.push(make_chart(mbc[i].chart_id, get_mbc_option(mbc[i].s_title, mbc[i].data, getArrayItems(color_list, color_list.length))));
           }

           for(var i in ebc){
              myChart.push(  make_chart( ebc[i].chart_id, get_ebc_option(ebc[i].s_title, ebc[i].data, 'normal') ) );
           }
           //interval = window.setTimeout(getdata.poll, update_time);
        },
        onError: function(){
           alert('参数传入错误!');
           return false;
        }
    };
    getdata.poll();
}


send_info();


/*    require([theme_path + defaultTheme], function(tarTheme){
         curTheme = tarTheme;
         refreshTheme();
    })
*/


var themeSelector = $('#theme-select');
if (themeSelector) {
    themeSelector.html(
        '<option selected="true" name="macarons">macarons</option>'
        + '<option name="infographic">infographic</option>'
        + '<option name="shine">shine</option>'
        + '<option name="dark">dark</option>'
        + '<option name="blue">blue</option>'
        + '<option name="green">green</option>'
        + '<option name="red">red</option>'
        + '<option name="gray">gray</option>'
        + '<option name="helianthus">helianthus</option>'
        + '<option name="roma">roma</option>'
        + '<option name="mint">mint</option>'
        + '<option name="macarons2">macarons2</option>'
        + '<option name="sakura">sakura</option>'
        + '<option name="default">default</option>'
    );
    $(themeSelector).on('change', function(){
        selectChange($(this).val());
    });
    function selectChange(value){
        var theme = value;
        //myChart.showLoading();
        //showloading();
        $(themeSelector).val(theme);
        if (theme != 'default') {
            require([theme_path + theme], function(tarTheme){
                curTheme = tarTheme;
                refreshTheme();
            })
        }
        else {
            curTheme = {};
            refreshTheme();
        }
    }

    $(themeSelector).val(defaultTheme);
    selectChange(defaultTheme)
}


