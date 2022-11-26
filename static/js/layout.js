function showmodal(string,time=4000) {
    document.getElementById("message").innerHTML = string;
    $('#messagemodal').modal('show');
    setTimeout(function() {
        $('#messagemodal').modal('hide')
    }, time);
}

function check_login_status() {
    if (session_logged_in == false) {
        $('#signinmodal').modal('show');
        return false;
    } else {
        return true;
    }
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

function deletenotification(element) {
    $.ajax({
        url: 'deletenotification',
        method: 'POST',
        data: {
            notificationid: element.id
        },
        success: function(response) {
            if (response == 'Successful') {
                element.parentNode.parentNode.parentNode.remove();
                let c = document.getElementById('notification-count')
                c.innerHTML = parseInt(c.innerHTML) - 1
            }
        }
    });
}

function forgotpassword(element) {
    email = document.getElementById('emailforsignin').value.trim()
    console.log('hi')
    if(email=="" || email==null)
    {
        showmodal('Fill in the email to proceed.')
    }
    else{
        $.ajax({
            url: 'forgotpassword',
            method: 'POST',
            data:{email:email},
            success:function(response){
                showmodal(response)
            }
        });
    }
}

