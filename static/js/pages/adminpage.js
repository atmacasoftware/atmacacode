/*Dark Mode Toggle*/

let darkmode_toggle = $(".dark-mode");
let darkMode = localStorage.getItem('dark');

const enableDarkMode = () => {
    //1. add the class darkmode to the body
    $('body').addClass('bg-dark');
    $('.top-bar').addClass('container-dark');
    $('.mat-card').addClass('container-dark');
    //2.update darkmode in the localStorage
    localStorage.setItem('dark', 'enabled')
}

const disableDarkMode = (e) => {
    //1. add the class darkmode to the body
    $('body').removeClass('bg-dark')
    $('.top-bar').removeClass('container-dark');
    $('.mat-card').removeClass('container-dark');
    //2.update darkmode in the localStorage
    localStorage.setItem('dark', null);
}

if (darkMode === 'enabled') {
    enableDarkMode();
}

darkmode_toggle.click(function (e) {
    let darkMode = localStorage.getItem('dark');
    e.preventDefault();
    if (darkMode !== "enabled") {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
});

//Responsive Dashboard

//$(window).resize(function () {
//    if ($(window).width() < 992) {
//        $(".sidebar").css({"transform": "translate3d(-100%,10px,10px)"});
//        $('.toggler').click(function (e) {
//            $('.sidebar').css({"transform": "translateZ(0)"});
//            $(".page-content").css({"margin-left": "0"});
//            e.stopPropagation();
//            $(window).click(function () {
//                $(".sidebar").css({"transform": "translate3d(-100%,10px,10px)"});
//            })
//        })
//    }else{
//        $(".sidebar").css({"transform": "translate3d(0,0,0)"});
//        $('.toggler').click(function (e) {
//            $(".sidebar").toggleClass("trans");
//            $('.page-content').toggleClass('ml-0')
//        })
//    }
//})
//
//$(window).bind('resize', function (){
//    if($(this).width() < 992){
//        $(".sidebar").css({"transform": "translate3d(-100%,10px,10px)"});
//        $('.page-content').css({"margin-left":"0"});
//    }else {
//        $(".sidebar").css({"transform": "translate3d(0,0,0)"});
//        $('.page-content').css({"margin-left":"0"});
//    }
//})
//



