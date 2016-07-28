var id = ''
var url = ''
function del_id(i,u){
    $('#delAlert').html('Are you want to delete it ?');
    id=i ;
    url=u;
}

function del_sure(){
    $.ajax({
        url: url,
        type: "POST",
        data: "",
        dataType: "text",
        success: function(data) {
            var obj = jQuery.parseJSON(data);
            if ( obj['res'] == 0 ){
                location.reload()
            } else {
                 meg = data['meg'];
                 $('#delAlert').html(meg);
                 $('#delButton').html('<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>')
            }

        },
        error: function(data) {
            form_code = 'ERROR : Delete Failed , Please contact the Admin to solve this question!';
            $('#delAlert').html(form_code);
            $('#delButton').html('<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>')
        }
    });
}

function has_key(dict, name){
    for(var key in dict){
        if (key == name){
            return 1;
        }
    }
    return 0;
}


function new_del_sure(){
    $.ajax({
        url: url,
        type: "POST",
        data: "",
        dataType: "text",
        success: function(data) {
            var obj = jQuery.parseJSON(data);
            if ( obj['res'] == 0 ){
                if ( has_key(obj, 'redirect_url') == 1){
                    location.href = obj['redirect_url']
                } else {
                    location.reload()
                }
            } else {
                 meg = data['meg'];
                 $('#delAlert').html(meg);
                 $('#delButton').html('<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>')
            }

        },
        error: function(data) {
            form_code = 'ERROR : Delete Failed , Please contact the Admin to solve this question!';
            $('#delAlert').html(form_code);
            $('#delButton').html('<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>')
        }
    });
}