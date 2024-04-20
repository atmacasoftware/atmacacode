(function ($) {
  "use strict";

/*---------------------------
    Hero Slider Activation
  -----------------------------------*/
  var swiper = new Swiper(".sliderone", {
    slidesPerView: 1,
    spaceBetween: 30,
    centeredSlides: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });

/* ----------------------------
    Tilt Animation 
-------------------------------*/
  $('.js-tilt').tilt({
      base: window,
      reset: true, 
      scale: 1.02, 
      reverse: true, 
      max: 15, 
      perspective: 3e3, 
      speed: 4e3
  });

/* ----------------------------
Odometer Activation 
-------------------------------*/
if( $('.odometer').length ){
  var elemOffset = $('.odometer').offset().top;
  var winHeight = $(window).height();
  if(elemOffset < winHeight){
    $('.odometer').each(function(){
      $(this).html($(this).data('count-to'));
    });
  }
  $(window).on('scroll', function(){
    var elemOffset = $('.odometer').offset().top;
    function winScrollPosition() {
      var scrollPos = $(window).scrollTop(),
        winHeight = $(window).height();
      var scrollPosition = Math.round(scrollPos + (winHeight / 1.2));
      return scrollPosition;
    }
    if ( elemOffset < winScrollPosition()) {
      $('.odometer').each(function(){
        $(this).html($(this).data('count-to'));
      });
    }	
  });
};

/* ----------------------------
Isotope Activation 
-------------------------------*/
$('.grid').imagesLoaded( function() {
    // filter items on button click
    $('.portfolio-menu-active').on( 'click', 'button', function() {
        var filterValue = $(this).attr('data-filter');
        $grid2.isotope({ filter: filterValue });
    });	
    // init Isotope
    var $grid2 = $('.grid').isotope({
        itemSelector: '.grid-item',
        percentPosition: true,
        layoutMode: 'masonry',
        masonry: {
            // use outer width of grid-sizer for columnWidth
            columnWidth: '.grid-item',
        }
    });
});
$('.isotope-btn-add-active button').on('click', function(event) {
    $(this).siblings('.active').removeClass('active');
    $(this).addClass('active');
    event.preventDefault();
});

/*---------------------------
  Testimonial Activation
-----------------------------------*/
var swiper = new Swiper(".testimonialone", {
  slidesPerView: 1,
  spaceBetween: 30,
  centeredSlides: true,
  pagination: false,
  allowTouchMove: true,
  
  navigation: {
    nextEl: '.testimonialone .swiper-btn-next',
    prevEl: '.testimonialone .swiper-btn-prev',
  },
});
/*---------------------------
  Testimonial Two Activation
-----------------------------------*/
var swiper = new Swiper(".testimonialtwo", {
  slidesPerView: 3,
  loop:true,
  pagination: false,
  allowTouchMove: true,
  navigation: false,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  breakpoints:{
    0: {
      slidesPerView: 1
    },
    480: {
      slidesPerView: 1
    },
    768: {
      slidesPerView: 2
    },
    992: {
      slidesPerView: 2
    },
    1200: {
      slidesPerView: 3
    }
  }
});
/*---------------------------
  Brand Slider Activation
-----------------------------------*/
var swiper = new Swiper(".brand-slider",{
  loop:true,
  speed:800,
  autoplay:false,
  slidesPerView:5,
  spaceBetween:0,
  pagination:false,
  navigation:false,
  breakpoints:{
    0: {
      slidesPerView: 2,
      spaceBetween: 80,
    },
    480: {
      slidesPerView: 2,
      spaceBetween: 140,
    },
    768: {
      slidesPerView: 3,
      spaceBetween: 140,
    },
    992: {
      slidesPerView: 3,
      spaceBetween: 200,
    },
    1200: {
      slidesPerView: 5,
      spaceBetween: 140,
    }
  }
})
/*---------------------------
  Brand Slider Two Activation
-----------------------------------*/
var swiper = new Swiper(".brand-slider-two",{
  loop:true,
  speed:800,
  autoplay:false,
  slidesPerView:4,
  spaceBetween:0,
  pagination:false,
  navigation:false,
  breakpoints:{
    0: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    480: {
      slidesPerView: 2,
      spaceBetween: 60,
    },
    768: {
      slidesPerView: 3,
      spaceBetween: 80,
    },
    992: {
      slidesPerView: 3,
      spaceBetween: 100,
    },
    1200: {
      slidesPerView: 4,
      spaceBetween: 110,
    }
  }
})

/*---------------------------
  Portfolio Carousel Activation
-----------------------------------*/
var swiper = new Swiper(".portfolio-carousel",{
  loop:true,
  slidesPerView:3,
  spaceBetween:20,
  pagination:false,  
  navigation: {
    nextEl: '.portfolio-carousel-wrapper .swiper-btn-next',
    prevEl: '.portfolio-carousel-wrapper .swiper-btn-prev',
  },
  breakpoints:{
    0: {
      slidesPerView: 1
    },
    480: {
      slidesPerView: 2
    },
    768: {
      slidesPerView: 3
    },
    992: {
      slidesPerView: 3
    },
    1200: {
      slidesPerView: 3
    }
  }
})

/*-------------------------------
FancyBox Activation
-----------------------------------*/
$('.video-popup').fancybox();


})(jQuery);