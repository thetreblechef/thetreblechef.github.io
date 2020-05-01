$(document).ready(function() {

$( ".toggle-genre" ).click(function() {
    $( ".genre-badge" ).toggle( "slow", function() {});
    
    var text = $('.toggle-genre').text();
    $('.toggle-genre').text(
        text == "Show Genres" ? "Hide Genres" : "Show Genres");
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$('.region-button').click(function(){
    if($(this).hasClass('rb-active')){
        $(".region-button").removeClass("rb-active");
        $(this).removeClass('rb-active')
    } else {
        $(".region-button").removeClass("rb-active");
        $(this).addClass('rb-active')
    }

    $('.card-region').hide();
    $('.card-top-release').hide();

    // Home Page
    if($(this).hasClass('rb-pf')){
        $('.card-pf').show();
    }else if($(this).hasClass('rb-am')){
        $('.card-am').show();
    }

    // Canada Page
    if($(this).hasClass('rb-tor')){
        $('.card-tor').show();
    }else if($(this).hasClass('rb-mon')){
        $('.card-mon').show();
    }else if($(this).hasClass('rb-wes')){
        $('.card-wes').show();
    }else if($(this).hasClass('rb-pra')){
        $('.card-pra').show();
    }else if($(this).hasClass('rb-ont')){
        $('.card-ont').show();
    }else if($(this).hasClass('rb-que')){
        $('.card-que').show();
    }else if($(this).hasClass('rb-atl')){
        $('.card-atl').show();
    }
});

});
