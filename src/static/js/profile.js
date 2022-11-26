$(window).on("load resize", function() {
    if ($(window).width() < 768) {
        $('.tab-menu').removeClass('flex-column');
        $('.side-bar').addClass('top-bar').removeClass('side-bar');
    } else {
        $('.tab-menu').addClass('flex-column');
        $('.top-bar').addClass('side-bar').removeClass('top-bar');
    }
});


let loadFile = function(event) {
    let output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
    }
    document.getElementById('update_btn').removeAttribute('disabled');
};

let options = document.getElementsByClassName('gender-option');
let i = 0;
for (i = 0; i < options.length; i++) {
    if (options[i].value === gender) {
        options[i].setAttribute('selected', true);
    }
}

function upload_avatar() {
    let files = document.getElementById('image_file').files;
    if (files.length < 1) {
        alert('Select atleast one file');
    } else {
        document.getElementById('update_btn').setAttribute('disabled', true);
        document.getElementById('update_btn').innerHTML = 'Updating..';
        let fd = new FormData();
        fd.append('img_file', files[0]);
        $.ajax({
            url: 'upload_avatar',
            method: 'POST',
            data: fd,
            processData: false, //add this
            contentType: false,
            success: function(msg) {
                document.getElementById('update_btn').innerHTML = 'Update';
                document.getElementById('remove_btn').removeAttribute('disabled');
            }
        });
    }
}

function remove_avatar() {
    $.ajax({
        url: 'remove_avatar',
        success: function(msg) {
            document.getElementById('remove_btn').setAttribute('disabled', true);
        }
    });
    document.getElementById('output').src = "../static/images/user-photo.png";
}