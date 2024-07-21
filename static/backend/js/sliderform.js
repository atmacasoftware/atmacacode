$(document).ready(function () {

    $(".button__text").hide()
    $(".button__url").hide()

    if ($('[name="redirecting_radio"]').is(':checked')) {
        $(".text-content").hide()
        $(".button__text").show()
        $(".detail__img").hide()
        $(".button__url").show()
    }

    $('[name="redirecting_radio"]').change(function () {
        if ($(this).is(':checked')) {
            $(".text-content").hide()
            $(".button__text").show()
            $(".detail__img").hide()
            $(".button__url").show()
        } else {
            $(".text-content").show()
            $(".button__text").hide()
            $(".detail__img").show()
            $(".button__url").hide()
        }

    });
})