(function ($) {
    "use strict";

 /*----------------------------------------
  Sticky Header Activation
  ------------------------------------------*/
  $(window).on('scroll', function () {
    if ($(this).scrollTop() > 0) {
      $('.sticky-header').addClass('sticky');
    } else {
      $('.sticky-header').removeClass('sticky');
    }
  });

  /*--------------------------------
      Custom script to call Background
      Image & Color from html data attribute
  -----------------------------------*/
  $('[data-bg-image]').each(function () {
    var $this = $(this),
        $image = $this.data('bg-image');
    $this.css('background-image', 'url(' + $image + ')');
  });
  $('[data-bg-color]').each(function () {
      var $this = $(this),
          $color = $this.data('bg-color');
      $this.css('background-color', $color);
  });

/*---------------------------------
  Parallax Instance
-----------------------------------*/

document.addEventListener("mousemove", parallax);
function parallax(e){
  this.querySelectorAll('.layer').forEach(function(layer){
    const speed = Number(layer.getAttribute('data-speed'))

    const x = (window.innerWidth - e.pageX*speed)/120
    const y = (window.innerHeight - e.pageY*speed)/120

    layer.style.transform = 'translateX('+x+'px) translateY('+y+'px)'
  })
}
/*----------------------------------------
    Responsive Mobile Menu
  ------------------------------------------*/
  var $offCanvasNav = $('.mobile-menu'),
  $offCanvasNavSubMenu = $offCanvasNav.find('.dropdown');
    /*Add Toggle Button With Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.parent().prepend('<span class="menu-expand"><i class="fas fa-angle-down"></i></span>');
    /*Close Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.slideUp();
    /*Category Sub Menu Toggle*/
    $offCanvasNav.on('click', 'li a, li .menu-expand', function(e) {
    var $this = $(this);
    if (($this.parent().attr('class').match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/)) && ($this.attr('href') === '#' || $this.hasClass('menu-expand'))) {
        e.preventDefault();
        if ($this.siblings('ul:visible').length) {
            $this.parent('li').removeClass('active');
            $this.siblings('ul').slideUp();
        } else {
            $this.parent('li').addClass('active');
            $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
            $this.closest('li').siblings('li').find('ul:visible').slideUp();
            $this.siblings('ul').slideDown();
        }
    }
});
/*---------------------------
    WOW Activation
  -----------------------------------*/
  new WOW(
    {
      once: true,
      mobile: false,
    }
  ).init();

  /*----------------------------------------*/
  /*  Scroll to top
  /*----------------------------------------*/
  function scrollToTop() {
    var $scrollUp = $('#scroll-top'),
      $lastScrollTop = 0,
      $window = $(window);
    $window.on('scroll', function () {
      var st = $(this).scrollTop();
      if (st > $lastScrollTop) {
          $scrollUp.removeClass('show');
      } else {
        if ($window.scrollTop() > 200) {
            $scrollUp.addClass('show show-active');
        } else {
            $scrollUp.removeClass('show show-active');
        }
      }
      $lastScrollTop = st;
    });

    $scrollUp.on('click', function (evt) {
      $('html, body').animate({scrollTop: 0}, 600);
      evt.preventDefault();
    });
  }
  scrollToTop();

    /*---------------------------------
	 	MailChimp
    -----------------------------------*/
    $("#mc-form").ajaxChimp({
      language: "en",
      callback: mailChimpResponse,
      // ADD YOUR MAILCHIMP URL BELOW HERE!
      url: "YOUR MAILCHIMP LINK HERE",
    });
    function mailChimpResponse(resp) {
      if (resp.result === "success") {
        $(".mailchimp-success")
          .html("" + resp.msg)
          .fadeIn(900);
        $(".mailchimp-error").fadeOut(400);
      } else if (resp.result === "error") {
        $(".mailchimp-error")
          .html("" + resp.msg)
          .fadeIn(900);
      }
    }

    /*---------------------------------
	 	Magnific pupup
    -----------------------------------*/
    $('.parent-gallery').magnificPopup({
      delegate: '.item', // child items selector, by clicking on it popup will open
      type: 'image',
      gallery:{
        enabled:true
      }
      // other options
    });

})(jQuery);