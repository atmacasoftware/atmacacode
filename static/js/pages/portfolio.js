(function ($) {
    "use strict";
  
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
  
})(jQuery);