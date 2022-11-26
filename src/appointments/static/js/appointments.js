function navbar_color() {
    if ($(document).scrollTop() < 1) {
        if ($("#collapse_target").hasClass("show")) {
            $(".navbar").css("background-image", "none");
        } else {
            $(".navbar").css("background-image", "linear-gradient(315deg, #f9d29d 0%, #fdc1ac 74%)");
        }
    }
};

$(function() {
    $(document).scroll(function() {
        var $nav = $(".navbar");
        if ($(window).width() < 576) {
            $nav.toggleClass('scrolled', $(this).scrollTop() > 1);
        } else {
            $nav.toggleClass('scrolled', $(this).scrollTop() > ($(window).height()) * 0.2);
        }
    });
});

$(".booknow-form30").submit(function() {
    var isFormValid = true;

    $(".form-control.30").each(function() {
        if ($.trim($(this).val()).length == 0) {
            $(this).parent().parent().children(0).css("color", "red");
            isFormValid = false;
        } else {
            $(this).parent().parent().children(0).css("color", "black");
        }
    });

    if (!isFormValid) alert("Please fill in all the highlighted fields");

    return isFormValid;
});

$(".booknow-form60").submit(function() {
    var isFormValid = true;

    $(".form-control.60").each(function() {
        if ($.trim($(this).val()).length == 0) {
            $(this).parent().parent().children(0).css("color", "red");
            isFormValid = false;
        } else {
            $(this).parent().parent().children(0).css("color", "black");
        }
    });

    if (!isFormValid) alert("Please fill in all the highlighted fields");

    return isFormValid;
});

$(".reschedule-form").submit(function() {
    var isFormValid = true;

    $(".form-control.RS").each(function() {
        if ($.trim($(this).val()).length == 0) {
            $(this).parent().parent().children(0).css("color", "red");
            isFormValid = false;
        } else {
            $(this).parent().parent().children(0).css("color", "black");
        }
    });

    if (!isFormValid) alert("Please fill in all the highlighted fields");

    return isFormValid;
});

// ------------------------------- Form Functions -------------------------------------

timepicker30 = document.getElementById('timepicker30')
timepicker60 = document.getElementById('timepicker60')
datepicker30 = document.getElementById('datepicker30')
datepicker60 = document.getElementById('datepicker60')
datepickerRS = document.getElementById('datepickerRS')
datepickerRS = document.getElementById('datepickerRS')


timepicker30.setAttribute('disabled', true);
datepicker30.setAttribute('disabled', true);
timepicker60.setAttribute('disabled', true);
datepicker60.setAttribute('disabled', true);
timepickerRS.setAttribute('disabled', true);
datepickerRS.setAttribute('disabled', true);

$('.datepicker').each(function() { this.style.backgroundColor = '#e9ecef'; })

document.onkeydown = function(e) {
    return false;
}

function reset_form(X) {
    if (X == 30) {
        timepicker30.setAttribute('disabled', true);
        datepicker30.setAttribute('disabled', true);
    } else {
        timepicker60.setAttribute('disabled', true);
        datepicker60.setAttribute('disabled', true);
    }
}

$(document).ready(function() {
    $('input.timepicker').timepicker({
        timeFormat: 'h:mm p',
        interval: 30,
        minTime: '9:00 AM',
        maxTime: '5:00 PM',
        scrollbar: true,
        rebuild: true,
        disableTouchKeyboard: true
    });
    $('.datepicker').datepicker({
        dateFormat: "dd/mm/yy",
        minDate: minDate_from_server,
        autoclose: true,
    });
});

var days = {
    'Sunday': 0,
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6
}

function getAvailableDays30(element) {
    datepicker30.setAttribute('disabled', true)
    datepicker30.style.backgroundColor = '#e9ecef';
    datepicker30.value = null
    let tid = element.value;
    $.ajax({
        url: 'get_available_days',
        method: 'POST',
        data: {
            tid: tid
        },
        success: (data) => {
            data = JSON.parse(data)
            let mapped_available_days = []
            data.forEach((day) => {
                mapped_available_days.push(days[day])
            })
            $('#datepicker30').datepicker('destroy')
            $('#datepicker30').datepicker({
                dateFormat: "dd/mm/yy",
                minDate: minDate_from_server,
                autoclose: true,
                beforeShowDay: function(date) {
                    if (mapped_available_days.includes(date.getDay())) {
                        return [true]
                    } else {
                        return [false]
                    }
                }
            });
            datepicker30.removeAttribute('disabled')
            datepicker30.style.backgroundColor = '#ffffff';
        }
    });
}

function getAvailableSlots30(element) {
    timepicker30.setAttribute('disabled', true)
    timepicker30.value = null
    let date = element.value;
    $.ajax({
        url: 'get_available_slots',
        method: 'POST',
        data: {
            tid: document.getElementById('therapist30').value,
            date: date
        },
        success: (slots) => {
            slots = JSON.parse(slots)
            $('#timepicker30').timepicker({
                timeFormat: 'h:i A',
                interval: 30,
                minTime: slots['preferred']["Start-time"],
                maxTime: slots['preferred']["End-time"],
                'disableTimeRanges': slots['not-available'],
                rebuild: true,
                scrollbar: true,
                disableTouchKeyboard: true
            });
            timepicker30.removeAttribute('disabled')
        }
    });
}

function getAvailableDays60(element) {
    datepicker60.setAttribute('disabled', true)
    datepicker60.style.backgroundColor = '#e9ecef';
    datepicker60.value = null
    let tid = element.value;
    $.ajax({
        url: 'get_available_days',
        method: 'POST',
        data: {
            tid: tid
        },
        success: (data) => {
            data = JSON.parse(data)
            let mapped_available_days = []
            data.forEach((day) => {
                mapped_available_days.push(days[day])
            })
            $('#datepicker60').datepicker('destroy')
            $('#datepicker60').datepicker({
                dateFormat: "dd/mm/yy",
                minDate: minDate_from_server,
                autoclose: true,
                beforeShowDay: function(date) {
                    if (mapped_available_days.includes(date.getDay())) {
                        return [true]
                    } else {
                        return [false]
                    }
                }
            });
            datepicker60.removeAttribute('disabled')
            datepicker60.style.backgroundColor = '#ffffff';
        }
    });
}

function getAvailableSlots60(element) {
    timepicker60.setAttribute('disabled', true)
    timepicker60.value = null
    let date = element.value;
    $.ajax({
        url: 'get_available_slots',
        method: 'POST',
        data: {
            tid: document.getElementById('therapist60').value,
            date: date
        },
        success: (slots) => {
            slots = JSON.parse(slots)
            $('#timepicker60').timepicker({
                timeFormat: 'h:i A',
                interval: 30,
                minTime: slots['preferred']["Start-time"],
                maxTime: slots['preferred']["End-time"],
                'disableTimeRanges': slots['not-available'],
                rebuild: true,
                scrollbar: true,
                disableTouchKeyboard: true
            });
            timepicker60.removeAttribute('disabled')
        }
    });
}

function getAvailableDaysRS(therapistID, mdate) {
    datepickerRS.setAttribute('disabled', true)
    datepickerRS.style.backgroundColor = '#e9ecef';
    datepickerRS.value = null
    let tidRS = therapistID;
    $.ajax({
        url: 'get_available_days',
        method: 'POST',
        data: {
            tid: tidRS
        },
        success: (data) => {
            data = JSON.parse(data)
            let mapped_available_days = []
            data.forEach((day) => {
                mapped_available_days.push(days[day])
            })
            $('#datepickerRS').datepicker('destroy')
            $('#datepickerRS').datepicker({
                dateFormat: "dd/mm/yy",
                minDate: mdate,
                autoclose: true,
                beforeShowDay: function(date) {
                    if (mapped_available_days.includes(date.getDay())) {
                        return [true]
                    } else {
                        return [false]
                    }
                }
            });
            datepickerRS.removeAttribute('disabled')
            datepickerRS.style.backgroundColor = '#ffffff';
        }
    });
}

function getAvailableSlotsRS(element) {
    timepickerRS.setAttribute('disabled', true)
    timepickerRS.value = null
    let date = element.value;
    $.ajax({
        url: 'get_available_slots',
        method: 'POST',
        data: {
            tid: document.getElementById('tidRS').value,
            date: date
        },
        success: (slots) => {
            slots = JSON.parse(slots)
            $('#timepickerRS').timepicker({
                timeFormat: 'h:i A',
                interval: 30,
                minTime: slots['preferred']["Start-time"],
                maxTime: slots['preferred']["End-time"],
                'disableTimeRanges': slots['not-available'],
                rebuild: true,
                scrollbar: true,
                disableTouchKeyboard: true
            });
            timepickerRS.removeAttribute('disabled')
        }
    });
}

function reschedule(tid, mid, mdate, mtime) {
    document.getElementById('tidRS').value = tid
    document.getElementById('midRS').value = mid
    getAvailableDaysRS(tid, mdate)
}