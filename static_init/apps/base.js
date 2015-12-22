'use strict';
import $ from 'jquery';

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
