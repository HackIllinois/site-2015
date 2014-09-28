$(document).ready(function () {
    var scene = $('#scene')[0];
    var parallax = new Parallax(scene);

    var resizeWaves = function() {
        // Get aspect ratio of window
        var aspectRatio = $(this).height() / $(this).width();
        if (aspectRatio > 1.0) {
            // Page is horizontal
            $("#waves").css({
                width: aspectRatio*140 + 40 + "%",
                height: "auto"
            });
        } else {
            $("#waves").css({
                width: "140%",
                height: "auto"
            });
        }
    }
    
    $(window).resize(resizeWaves).ready(resizeWaves);
});
