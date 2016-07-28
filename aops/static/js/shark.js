function empty(v){
    switch (typeof v){
        case 'undefined' : return true;
        case 'string' : if(v.trim().length == 0) return true; break;
        case 'boolean' : if(!v) return true; break;
        case 'number' : if(0 === v) return true; break;
        case 'object' :
            if(null === v) return true;
            if(undefined !== v.length && v.length==0) return true;
            for(var k in v){return false;} return true;
            break;
    }
    return false;
}


window.onload = function()
{
    $.ajax({
        url: "/accounts/language/list/",
        type: "POST",
        data: "",
        dataType: "text",
        success: function(data) {
            var obj = jQuery.parseJSON(data);
            form_code = lang_select(obj);
            document.getElementById('language').innerHTML = form_code;
        },
        error: function(data) {
            form_code = '';
            document.getElementById('language').innerHTML = form_code;
        }
    });
}


function lang_select(data){
    var form_code='<option value="en">-----------</option>';

    now_s = data[1]
    for ( key in data[0] ) {
        if ( ! empty(data[0][key]) ){
            if ( key == now_s ){ 
                form_code = form_code + "<option value='"+ key +"' selected> "+ data[0][key] + "</option>";
            }else {
                form_code = form_code + "<option value='"+ key +"'> "+ data[0][key] + "</option>";
            }
        }
    }
    return form_code;
}


function on_change() {
        s_value = $('#language').val();
        $.ajax({
            url: "/accounts/language/select/",
            type: "POST",
            data: {"language":s_value},
            dataType: "text",
            success: function(data) {
                location.reload();
            },
            error: function(data) {
                alert('Error');
            }
        });
}


function setCookie(name,value,expires)
{
    document.cookie = name + "="+ escape (value) + ";expires='" + expires+"';path=/";
} 


function getCookie(name)
{
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
 
    if(arr=document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
} 


function getAutoVal(s_id, url, d_type) {
    var getdata;
    var send_data = {'d_type':d_type};
    getdata = {
        poll: function(){
            $.ajax({url: url,
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
           document.getElementById(s_id).value = data.val;
           var fields = data.fields
        },
        onError: function(){
           alert('参数传入错误!');
           return false;
        }
    };
    getdata.poll();
}


