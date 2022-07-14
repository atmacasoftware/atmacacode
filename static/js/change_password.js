$("#alert-notcompatible").hide();
$("#alert-compatible").hide();

$("#changePassword").focusout(function () {
    var special_characters = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;
    let a = $("#password").val();
    let b = $("#re-password").val();
    if (a === b) {
        if (a.length >= 8) {
            $(".rules1").css('color', 'green');
            if (a.match(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/)) {
                if (a.match(special_characters)) {
                    $("#changePassword").removeAttr("disabled");
                    $("#alert-compatible").show();
                    $("#alert-notcompatible").hide();
                } else {
                    $("#alert-notcompatible").show();
                    $("#alert-compatible").hide();
                }
            } else {
                $("#alert-notcompatible").show();
                $("#alert-compatible").hide();
            }
        } else {
            $("#alert-notcompatible").show();
            $("#alert-compatible").hide();
        }
    } else {
        $("#changePassword").prop("disabled", true);
        $("#alert-notcompatible").show();
    }

});


