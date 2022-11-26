$('.textarea-format').each(function() {
    this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

function likestory(element) {

    if (check_login_status()) {

        no_of_likes = element.querySelector('span').innerHTML;

        if (element.querySelector('i').classList.contains('liked')) {
            element.querySelector('i').classList.remove('liked', 'fa-heart');
            element.querySelector('i').classList.add('fa-heart-o');
            element.querySelector('span').innerHTML = parseInt(no_of_likes) - 1;
            $.ajax({
                url: 'likestory',
                method: 'POST',
                data: {
                    increment: -1,
                    storyid: element.id
                }
            });
        } else {
            element.querySelector('i').classList.remove('fa-heart-o');
            element.querySelector('i').classList.add('fa-heart', 'liked');
            element.querySelector('span').innerHTML = parseInt(no_of_likes) + 1;
            $.ajax({
                url: 'likestory',
                method: 'POST',
                data: {
                    increment: 1,
                    storyid: element.id
                }
            });
        }
    }

}

toTopbtn = document.getElementById("backtoTop");
window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        toTopbtn.style.display = "block";
    } else {
        toTopbtn.style.display = "none";
    }
}

function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

let comments_div = document.getElementsByClassName('comment-section')[0]

function load_more_comments(element){
    element.innerHTML='Loading...'
    element.disabled = true
    element.classList.add('loading')

    $.ajax({
        url:'load_more_comments',
        data:{storyid: element.id},
        method:'post',
        success:function(response){
            more_comments = JSON.parse(response)
            if(Object.keys(more_comments).length == 0){
                element.style.display='none'
                return false
            }
            Object.keys(more_comments).forEach(cid => {
                    let div = document.createElement('div')
                    div.innerHTML= `<div class="user-img-div-cmt col-1">
                                        <img class="user-image-comments" src="static/images/user-photo.png" alt="">
                                    </div>
                                    <div class="comment-text col-11">
                                        <h4 class="comment-nickname">${more_comments[cid]['Nickname']}</h4>
                                        <p>${more_comments[cid]['Comment-Body']}</p>
                                    </div>`
                    div.className = 'comment row'
                    comments_div.appendChild(div)
            })
            element.innerHTML='Load more'
            element.disabled = false
            element.classList.remove('loading')
        }
    })
}