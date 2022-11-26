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

let stories_div = document.getElementsByClassName('stories')[0]
let loadmore_btn = document.getElementsByClassName('loadmore')[0]
let hr = document.createElement('hr')

function load_more_stories(){
        loadmore_btn.disabled = true
        loadmore_btn.innerHTML='Loading...'
        loadmore_btn.classList.add('loading')

        $.ajax({
            url:'load_more_stories',
            method:'post',
            success:function(response){
                more_stories = JSON.parse(response)
                if(Object.keys(more_stories).length == 0){
                    loadmore_btn.style.display='none'
                    return false
                }
                Object.keys(more_stories).forEach(key => {
                    Object.keys(more_stories[key]).forEach(key2=>{
                    let liked
                    if('liked' in more_stories[key][key2]){
                        liked = `<i class="fa fa-heart liked"></i>`
                    }
                    else{
                        liked = `<i class="fa fa-heart-o"></i>`
                    }
                    comments_length=more_stories[key][key2]['Comment-count']

                    let div = document.createElement('div')
                    div.innerHTML= `<div class="col-sm-2 user-img-div">
                                            <img class="user-image" src="static/images/user-photo.png" alt="">
                                        </div>
                                        <div class="col-sm-10 story-text">
                                            <img class="user-image-mobile" src="static/images/user-photo.png" alt="">
                                            <a class="story-title" href="/story?sid=${key2}">${more_stories[key][key2]['Title']}</a>
                                            <p>${more_stories[key][key2]['Body']}</p>
                                            <div class="likes-comments">
                                                <button id="${key2}" class="btn btn-outline btn-like" onclick="likestory(this)">
                                                    ${liked}
                                                    <span>${more_stories[key][key2]['Likes']}</span>
                                                </button>
                                                <a class="btn btn-outline btn-comment" href="/story?sid=${key2}">
                                                    <i class="fa fa-comment-o"></i>
                                                    <span>
                                                        ${comments_length}    
                                                    </span>
                                                </a>
                                            </div>
                                        </div>
                                    <hr>`
                    div.className="row story-row"
                    div.id = key
                    stories_div.appendChild(div)
                    stories_div.appendChild(hr)
                })
            })
                loadmore_btn.disabled = false
                loadmore_btn.innerHTML='Load more<i class="fas fa-chevron-down"></i>'
                loadmore_btn.classList.remove('loading')
            }
        })
}
        