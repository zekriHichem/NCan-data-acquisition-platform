var i=0;
$('.card-bis-1').each(function (index) {
    i++;
});

if ( i <10){
    $('#end').hide();

} else{
    var j = 0;
    $('.card-bis-1').each(function (index) {
        if (j>10)
        {
            $(this).css("display","none");
            $(this).addClass("h");
        }
        j++;

    });


    $('#end').on('click',function () {
        var k =0;
        var e = 0;
        $('.h').each(function (index) {
            if ( k <10){
                e++;
            $(this).css('display','block');
            $(this).removeClass('h');
            }
            k++;
        })

        if ( k-e == 0 )
            $('#end').hide();

    });

}


