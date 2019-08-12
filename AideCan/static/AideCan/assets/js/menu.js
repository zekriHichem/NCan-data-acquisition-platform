var i =0;
console.log("hello")
$('#burger-col').on('click',function () {
    console.log("world")
    i++;

    if (i % 2 == 0){
    $('.menu-b-item').css("display","none");
}else {
    $('.menu-b-item').css("display","block");

}


})



$(window).resize(function(){

    if ($(window).width() > 991) {
        $('.menu-b-item').css("display","block");
        $('#rigestration-b').css("display","none");
        $('#login-b').css("display","none");
        i=0;
    }

    if ((i == 0)  && ($(window).width() < 991)){
        $('.menu-b-item').css("display","none");
    }


});


