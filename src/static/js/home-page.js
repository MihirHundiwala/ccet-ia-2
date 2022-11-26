function navbar_color() {
    if ($(document).scrollTop() < 1) {
        if ($("#collapse_target").hasClass("show")) {
            $(".navbar").css("background-image", "none");
        } else {
            $(".navbar").css("background-image", "linear-gradient(145deg, #00b4c6 0%, #0088e8 100%)");
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

$(window).on("load", function() {

    $("#preloader").animate({
            opacity: "0"
        },
        900,
        function() {
            setTimeout(function() {
                $("#preloader")
                    .css("visibility", "hidden")
                    .fadeOut();
            }, 400);
        }
    );
});