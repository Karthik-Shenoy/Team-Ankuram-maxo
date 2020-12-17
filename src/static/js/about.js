$(document).ready(function() {
    $('.card').hover(function() {
        $(this).addClass('flipped');
    }, function() {
        $(this).removeClass('flipped');
    });
});