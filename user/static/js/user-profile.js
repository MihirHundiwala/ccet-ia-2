$(document).ready(() => {
    $.ajax({
        url: '/user/getmeetings',
        method: 'GET',
        success: (m) => {
            console.log(Object.keys(m['m']).length)
            if (Object.keys(m['m']).length) {
                Object.entries(m['m']).forEach(([key, value]) => {
                    meet = document.createElement('div')
                    meet.innerHTML = `<div class="col-2 col-md-1 profile-icon-col"><img src="/static/images/video-icon.png" alt=""></div>
						                <div class="col-10 col-md-11 profile-text-col">
						                    <p>Scheduled with ${value['TherapistName']}</p>
						                    <p class="profile-text-time" style="font-size: 13px !important;">On ${value['Date']}, ${value['Time']}</p>
						                </div>`
                    meet.className = "row align-items-center profile-item-row"
                    document.getElementById('meetings-div').appendChild(meet)
                })
            } else {
                document.getElementById('meetings-div').innerHTML += `<h3 class="empty-area-text">No Upcoming Sessions!</h3>`
            }

            if (Object.keys(m['p']).length) {
                Object.entries(m['p']).forEach(([key, value]) => {
                    meet = document.createElement('div')
                    meet.innerHTML = `<div class="col-2 col-md-1 profile-icon-col"><img src="/static/images/video-icon.png" alt=""></div>
			                            <div class="col-10 col-md-11 profile-text-col">
			                                <p>Was Scheduled with ${value['TherapistName']}</p>
			                                <p class="profile-text-time" style="font-size: 13px !important;">On ${value['Date']}, ${value['Time']}</p>
			                            </div>`
                    meet.className = "row align-items-center profile-item-row"
                    document.getElementById('past-meetings-div').appendChild(meet)
                })
            } else {
                document.getElementById('past-meetings-div').innerHTML += `<h3 class="empty-area-text">No Past Sessions!</h3>`
            }
        }
    });
})