$(document).ready(function () {
    var scene = $('#scene')[0];
    var parallax = new Parallax(scene);

    var resizeWaves = function() {
        // Get aspect ratio of window
        var aspectRatio = $(this).width() / $(this).height();
        if (aspectRatio > 1.2) {
            // Page is horizontal
            $("#waves").css({
                width: "120%",
                height: "auto"
            });
        } else if (aspectRatio < 1.2) {
            // Page is vertical
            $("#waves").css({
                height: "120%",
                width: "auto"
            });
        }
    }
    
    $(window).resize(resizeWaves).ready(resizeWaves);
});
