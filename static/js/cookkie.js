/*Dark Mode Toggle*/
let cerez = document.querySelector('.cerez-container');
let cerezClose = document.querySelector('.cerez-close');
let activeCerez = localStorage.getItem('active');

const cerezMode = () => {
    cerez.classList.add('passive')
    //2.update darkmode in the localStorage
    localStorage.setItem('active', 'enabled');
}

const disableCerezMode = (e) => {
    //1. add the class darkmode to the body
    cerez.classList.remove('passive')

    //2.update darkmode in the localStorage
    localStorage.setItem('active', null);
}

if (activeCerez === 'enabled') {
    cerezMode();
}

cerezClose.addEventListener("click", (e) => {
    let activeCerez = localStorage.getItem('active');
    e.preventDefault();
    if (activeCerez !== "enabled") {
        cerezMode();
    } else {
        disableCerezMode();
    }
});