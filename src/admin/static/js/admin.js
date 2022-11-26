function approvestory(element) {
    $.ajax({
        url: 'approvestory',
        method: 'POST',
        data: {
            storyid: element.id
        },
        success: function(response) {
            if (response == 'Successful') {
                element.parentNode.parentNode.remove()
            }
        }
    });

}

function disapprovestory(element) {
    $.ajax({
        url: 'disapprovestory',
        method: 'POST',
        data: {
            storyid: element.id
        },
        success: function(response) {
            if (response == 'Successful') {
                element.parentNode.parentNode.remove()
            }
        }
    });

}

function approvecomment(element, storyid, commentid) {
    $.ajax({
        url: 'approvecomment',
        method: 'POST',
        data: {
            storyid: storyid,
            commentid: commentid,
        },
        success: function(response) {
            if (response == 'Successful') {
                element.parentNode.parentNode.parentNode.remove()
            }
        }
    });
}

function disapprovecomment(element, storyid, commentid) {
    $.ajax({
        url: 'disapprovecomment',
        method: 'POST',
        data: {
            storyid: storyid,
            commentid: commentid,
        },
        success: function(response) {
            if (response == 'Successful') {
                element.parentNode.parentNode.parentNode.remove()
            }
        }
    });
}