$(document).ready(function() {

$( ".toggle-genre-tor" ).click(function() {
    $( ".genre-tor" ).toggle( "slow", function() {});
    
    var text = $('.toggle-genre-tor').text();
    $('.toggle-genre-tor').text(
        text == "Show Genres" ? "Hide Genres" : "Show Genres");
});

$( ".toggle-genre-mon" ).click(function() {
    $( ".genre-mon" ).toggle( "slow", function() {});
    
    var text = $('.toggle-genre-mon').text();
    $('.toggle-genre-mon').text(
        text == "Show Genres" ? "Hide Genres" : "Show Genres");
});

$( ".toggle-genre-van" ).click(function() {
    $( ".genre-van" ).toggle( "slow", function() {});
    
    var text = $('.toggle-genre-van').text();
    $('.toggle-genre-van').text(
        text == "Show Genres" ? "Hide Genres" : "Show Genres");
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

});
