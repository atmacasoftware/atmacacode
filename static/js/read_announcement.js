const list = document.querySelectorAll('.list_announcement');

list.forEach(item => {
    $(item).click(function (){
        console.log(item)
    })
})