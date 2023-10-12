function is_checked(obj_id, state){
    $.ajax({
        type:"POST",
        url: "api/check",
        data: {
            'obj_id': obj_id,
            'state': state,
        },
        success: function(response){
            location.reload();
        }
    });
}

function add_new_target(member_id="KYUMIN", target_date="2023-10-10"){
    $.ajax({
        type:"POST",
        url: "api/add_new_target",
        data: {
            'member_id': member_id,
            'target_date' : target_date,
            'text': document.getElementById("created_text").value
        },
        success: function(response){
            location.reload();
        }
    });
}

function delete_item(obj_id){
    $.ajax({
        type:"POST",
        url: "api/delete_target",
        data: {
            'obj_id': obj_id
        },
        success: function(response){
            location.reload();
        }
    });
}