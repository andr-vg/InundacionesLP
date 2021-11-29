window.onload = function() {
    var check_icon = document.getElementById("checkbtn");
    check_icon.addEventListener("click", bringToFront);
    //check_icon.addEventListener
    //var forms = document.getElementsByClassName(".col.align-items-center");
    //forms = forms + document.getElementsByClassName(".col-sm-auto");
    //for (let form of forms) {
    //    form.addEventListener("checked", bringToBack);
    //    form.addEventListener("unchecked", bringToFront);
    //}
}

function bringToFront() {
    var forms = document.getElementsByClassName("col align-items-center");
    var forms2 = document.getElementsByClassName("col-sm-auto");
    if (this.style.zIndex == ""){
        this.style.zIndex = 10;       
        for (let form of forms){
            form.style.zIndex = -1;
        }       
        for (let form of forms2){
            form.style.zIndex = -1;
        }
    } else {
        // bring to back
        this.style.zIndex = "";
        for (let form of forms){
            console.log(form.style.zIndex);
            form.style.zIndex = 0;
        }
        for (let form of forms2){
            console.log(form.style.zIndex);
            form.style.zIndex = 0;
        }
    }
    
}