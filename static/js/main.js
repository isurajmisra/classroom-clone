$('.dropdown-trigger').dropdown();

$('.modal').modal();
$(document).ready(function() {
    $('.tabs').tabs();
});
$(document).ready(function() {
    $('select').formSelect();
});


function check() {
    if (document.querySelector("#shortA")) {
        document.querySelector("#shortL").style.display = "none";
        document.querySelector("#shortAns").style.display = "none";
        let btn = document.querySelector("#short")
        btn.setAttribute('disabled', true)
    }

}
check()

function checkO() {
    if (document.querySelector("#optionC")) {
        let btnId = document.querySelector("#q-pk").value

        let o = document.querySelectorAll("#optionM")
        o.forEach(e => {
            if (e.value == document.querySelector("#optionC").value) {
                e.style.display = 'none';
                e.nextElementSibling.style.display = 'none';
            }
        })
        let btn = document.getElementById(btnId);

        btn.setAttribute('disabled', true);
    }

}
checkO()