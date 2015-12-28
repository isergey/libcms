import 'owl-carousel';
const $ = window.$;

$('#owl-1').owlCarousel({
  autoPlay: true,
  stopOnHover: true,
  loop: true,
  autoWidth: true,
  slideSpeed: 100,
  items: 4,
  responsive: false,
  responsiveRefreshRate: 200,
});

$('#owl-2').owlCarousel({
  autoPlay: true,
  stopOnHover: true,
  loop: true,
  autoWidth: true,
  slideSpeed: 100,
  items: 4,
  responsive: false,
  responsiveRefreshRate: 200,
});

$('#owl-poster').owlCarousel({
  autoPlay: true,
  stopOnHover: true,
  loop: true,
  autoWidth: true,
  slideSpeed: 100,
  items: 1,
  responsive: false,
});
