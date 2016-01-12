'use strict';
const $ = window.$;

$('.click-nav > ul').toggleClass('no-js js');
$('.click-nav .js ul').hide();
$('.click-nav .js').click(function (e) {
  $('.click-nav .js ul').slideToggle(0);
  $('.clicker').toggleClass('active');
  e.stopPropagation();
});

$(document).click(function () {
  if ($('.click-nav .js ul').is(':visible')) {
    $('.click-nav .js ul', this).slideUp(0);
    $('.clicker').removeClass('active');
  }
});


$('.tab-container__tabs li').click(() => {
  if (!$(this).hasClass('active')) {
    const tabNum = $(this).index();
    const nthChild = tabNum + 1;
    $('.tab-container__tabs li.active').removeClass('active');
    $(this).addClass('active');
    $('.tab-container__tab li.active').removeClass('active');
    $('.tab-container__tab li:nth-child(' + nthChild + ')').addClass('active');
  }
});


$('.facet__header').click(function () {
  const facetBody = $(this).next();
  if (facetBody.hasClass('facet__body_closed')) {
    $(this).removeClass('facet__header_closed');
    facetBody.removeClass('facet__body_closed');
  } else {
    facetBody.addClass('facet__body_closed');
    $(this).addClass('facet__header_closed');
  }
});

// <!-- Ya map -->
// window.ymaps.ready(init);
// let myMap;
//
// function init() {
//  myMap = new ymaps.Map("map", {
//    center: [55.76, 37.64],
//    zoom: 7
//  });
// }



/*Go to index.html*/
//function getRandomArbitrary(min, max) {
//  return Math.random() * (max - min) + min;
//}

//$(function () {
//  const imgHead = [];
//
//  $('.bg-img img').each(function () {
//    imgHead.push($(this).attr('src'));
//  });
//
//  function csaHead() {
//    const $csaHead = $('.bg_first');
//    const index = Math.floor(getRandomArbitrary(0, imgHead.length));
//    $csaHead.css({ 'background': 'url(' + imgHead[index] + ') no-repeat #000' });
//    $csaHead.css({ 'background-position': 'center top' });
//    //$csaHead.css({ 'background-size': '100% auto' });
//  }
//
//  csaHead();
//  setInterval(csaHead, 5000);
//});

$(document).ready(function ($) {
  var offset = 300,
    offset_opacity = 1200,
    scroll_top_duration = 700,
    $back_to_top = $('.cd-top');
  $(window).scroll(function(){
    ( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
    if( $(this).scrollTop() > offset_opacity ) {
      $back_to_top.addClass('cd-fade-out');
    }
  });

  $back_to_top.on('click', function(event){
    event.preventDefault();
    $('body,html').animate({
        scrollTop: 0 ,
      }, scroll_top_duration
    );
  });

});



