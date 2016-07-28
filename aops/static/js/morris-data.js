$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            period: '2010 Q1',
            iphone: 2666,
            ipad: null,
            itouch: 2647
        }, {
            period: '2010 Q2',
            iphone: 2778,
            ipad: 2294,
            itouch: 2441
        }, {
            period: '2010 Q3',
            iphone: 4912,
            ipad: 1969,
            itouch: 2501
        }, {
            period: '2010 Q4',
            iphone: 3767,
            ipad: 3597,
            itouch: 5689
        }, {
            period: '2011 Q1',
            iphone: 6810,
            ipad: 1914,
            itouch: 2293
        }, {
            period: '2011 Q2',
            iphone: 5670,
            ipad: 4293,
            itouch: 1881
        }, {
            period: '2011 Q3',
            iphone: 4820,
            ipad: 3795,
            itouch: 1588
        }, {
            period: '2011 Q4',
            iphone: 15073,
            ipad: 5967,
            itouch: 5175
        }, {
            period: '2012 Q1',
            iphone: 10687,
            ipad: 4460,
            itouch: 2028
        }, {
            period: '2012 Q2',
            iphone: 8432,
            ipad: 5713,
            itouch: 1791
        }],
        xkey: 'period',
        ykeys: ['iphone', 'ipad', 'itouch'],
        labels: ['iPhone', 'iPad', 'iPod Touch'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });



    Morris.Donut({
        element: 'morris-donut-chart01',
        data: [{
            label: "运行",
            value: 100
        }, {
            label: "备用",
            value: 3
        }, {
            label: "报废",
            value: 8
        }],
        colors: ['#CC9EF7', '#9AED2F', '#F72E9D'],
        resize: true
    });


    Morris.Donut({
        element: 'morris-donut-chart02',
        data: [{
            label: "在线",
            value: 300
        }, {
            label: "备用",
            value: 10
        }, {
            label: "停机",
            value: 3
        }],
        colors: ['#F2EE8C', '#EDD41C', '#ED8610'],
        resize: true
    });


    Morris.Donut({
        element: 'morris-donut-chart03',
        data: [{
            label: "Download Sales",
            value: 12
        }, {
            label: "In-Store Sales",
            value: 30
        }, {
            label: "Mail-Order Sales",
            value: 20
        }],
        colors: ['#91E4F7', '#42F7EE', '#18F7BB'],
        resize: true
    });


    Morris.Donut({
        element: 'morris-donut-chart04',
        data: [{
            label: "Download Sales",
            value: 12
        }, {
            label: "In-Store Sales",
            value: 30
        }, {
            label: "Mail-Order Sales",
            value: 20
        }],
        resize: true
    });






    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: 'tomcat',
            a: 100,
            b: 90
        }, {
            y: 'mysql',
            a: 75,
            b: 65
        }, {
            y: 'postresql',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });



});
