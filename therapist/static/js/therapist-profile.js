let days = document.getElementById('days');
for (i = 0; i < days.length; i++) {
    if (daysfromdb.includes(days[i].value)) {
        days[i].setAttribute('selected', true);
    }
}

$(document).ready(function() {
    $('input.timepicker').timepicker({
        timeFormat: 'h:i A',
        interval: 60,
        minTime: '9:00 AM',
        maxTime: '9:00 PM',
        scrollbar: true,
        rebuild: true
    });
    var multipleCancelButton = new Choices('#days', {
        removeItemButton: true,
        maxItemCount: 7,
        searchResultLimit: 7,
        renderChoiceLimit: 7
    });

    $.ajax({
        url: '/therapist/getmeetings',
        method: 'GET',
        success: (meetings) => {
            if(Object.keys(meetings).length){
                Object.entries(meetings).forEach( ([key,value]) =>{
                    meet = document.createElement('div')
                    meet.innerHTML = `<div class="col-1 profile-icon-col"><img src="/static/images/video-icon.png" alt=""></div>
                                        <div class="col-11 profile-text-col">
                                            <p>Scheduled with ${value['UserNickname']}</p>
                                            <p class="profile-text-time" style="font-size: 13px !important;">On ${value['Date']}, ${value['Time']}</p>
                                        </div>`
                    meet.className = "row align-items-center profile-item-row"
                    document.getElementById('meetings-div').appendChild(meet)
                })
            }
            else{
                document.getElementById('meetings-div').innerHTML+=`<h3 class="empty-area-text">No Upcoming Sessions!</h3>`
            }
        }
    });
});

