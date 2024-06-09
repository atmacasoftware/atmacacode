const notificationItemDropdown = document.querySelector(".notifications-items");

function startLiveRefreshAnnouncement() {
    setInterval(function () {
        $(".notifications-items").empty();
        fetch("/bildirim-servisi/bildirim-yenile")
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data[0] === true) {
                    $(".notification-toggle").addClass("beep");
                }
                var notifications = data[1];
                if(notifications.length > 0){
                    notifications.map((items) => {
                    if (items["n_type"] == "Soru") {
                        var item = `<a href="<a href=/bildirim-servisi/bildirim/${items["id"]}" data-id = "${items["id"]}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-warning text-white">
                                    <i class="fas fa-send"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items["title"]}
                                    <div class="time text-primary">${items["passing_time"]}</div>
                                </div>
                            </a>`;
                    } else if (items["n_type"] == "Kayıt Onay") {
                        var item = `<a href="<a href=/bildirim-servisi/bildirim/${items["id"]}" data-id = "${items["id"]}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-primary text-white">
                                    <i class="fas fa-check"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items["title"]}
                                    <div class="time text-primary">${items["passing_time"]}</div>
                                </div>
                            </a>`;
                    } else if (items["n_type"] == "İş Teklifi") {
                        var item = `<a href="<a href=/bildirim-servisi/bildirim/${items["id"]}" data-id = "${items["id"]}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-secondary text-white">
                                    <i class="fas fa-cubes-stacked"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items["title"]}
                                    <div class="time text-primary">${items["passing_time"]}</div>
                                </div>
                            </a>`;
                    } else {
                        var item = `<a href="/bildirim-servisi/bildirim/${items["id"]}" data-id = "${items["id"]}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-dark text-white">
                                    <i class="fas fa-user-plus"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items["title"]}
                                    <div class="time text-primary">${items["passing_time"]}</div>
                                </div>
                            </a>`;
                    }
                    $(".notifications-items").append(item);
                });
                }else{
                    $(".notifications-items").html(
                        `
                            <div style="height: 100%;width: 100%; display: flex; justify-content: center; align-items: center;flex-direction: column;" class="bg-light">
                            <i class="fa fa-2x fa-exclamation-circle"></i>
                            <h6 class="text-center mt-2">Şu anda okunmamış bildiriminiz bulunmamaktadır.</h6>
                        </div>
                        `
                    )
                }

            })

    }, 60000);
}

document.addEventListener("DOMContentLoaded", function () {
    startLiveRefreshAnnouncement();
});

$(document).ready(function () {
    const allReadNotificationBtn = document.getElementById("allReadBtn");
    allReadNotificationBtn.addEventListener("click", function (e) {
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: "/bildirim-servisi/tumunu-okundu-olarak-isaretle",
            beforeSend: function () {
                $(".waiting").css("display", "flex");
                $(".waiting").css("visibility", "visible");
            },
            success: (res) => {
                $(".waiting").css("display", "none");
                $(".waiting").css("visibility", "hidden");
                window.location.reload();
            },
        });
    });
});
