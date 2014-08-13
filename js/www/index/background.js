function createParallax() {
    var scene = $('#scene')[0];
    var parallax = new Parallax(scene);
}

$(document).ready(function () {
    createParallax();
    $(window).resize(function () {
        // Get aspect ratio of window
        var aspectRatio = $(this).width() / $(this).height();
        if (aspectRatio > 1) {
            // Page is horizontal
            $("#waves").css({
                width: "120%",
                height: "auto"
            });
        } else if (aspectRatio < 1) {
            // Page is verticle
            $("#waves").css({
                height: "120%",
                width: "auto"
            });
        }
    });
});