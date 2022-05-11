(function ($) {
    "use strict";
  
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
  
})(jQuery);