function updateClock() {
    var now = new Date();
    var dname = now.getDay(),
        mo = now.getMonth(),
        dnum = now.getDate(),
        yr = now.getFullYear(),
        hou = now.getHours(),
        min = now.getMinutes();

    Number.prototype.pad = function (digits) {
        for (var n = this.toString(); n.length < digits; n = 0 + n) ;
        return n;
    }

    var months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
    var week = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"];
    var ids = ["dayname", "month", "daynum", "year", "hour", "minutes"];
    var values = [week[dname], months[mo], dnum.pad(2), yr, hou.pad(2), min.pad(2)];

    for (var i = 0; i < ids.length; i++) {
        document.getElementById(ids[i]).firstChild.nodeValue = values[i];
    }


}

function initClock() {
    updateClock();
    window.setInterval("updateClock()", 1)
}


$(document).ready(function () {

    function getData() {
        var url = "https://fcc-weather-api.glitch.me/api/current?";
        var latitude;
        var longitude;
        var havaDurumUrl;

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                latitude = position.coords.latitude;
                longitude = position.coords.longitude;
                havaDurumUrl = (url + "lat=" + latitude + "&lon=" + longitude);

                $.ajax({
                    url: havaDurumUrl,
                    dataType: 'json',
                    success: function (result) {

                        $("#place").text(result.name);
                        $("#country").text(result.sys.country);
                        $("#weatherMain").text(result.weather[0].main);
                        $("#weatherIcon").html("<img src= weatherIcon>");
                        $("#temperature").text(result.main.temp);
                        $("#tempMin").text(Math.round(result.main.temp_min));


                        var havaresmi = result.weather[0].main;

                        switch (havaresmi) {
                            case 'Clouds':
                                var element = document.getElementById("durumimg");
                                var src = element.getAttribute("data-clouds");
                                element.setAttribute("src", src);
                                break;
                            case 'Rains':
                                var element = document.getElementById("durumimg");
                                var src = element.getAttribute("data-rain");
                                element.setAttribute("src", src);
                                break;
                            case 'Clear':
                                var element = document.getElementById("durumimg");
                                var src = element.getAttribute("data-sun");
                                element.setAttribute("src", src);
                                break;
                        }

                        var c = result.main.temp_min;

                    }
                });
            });
        }

    }

    getData();


});