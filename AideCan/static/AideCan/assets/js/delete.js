
$(".deletbtn").on("click",function (e) {
    if (confirm("are you sure"))
        console.log("helo");
    else
        e.preventDefault();
})