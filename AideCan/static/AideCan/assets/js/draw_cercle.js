  //Canvas
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    //Variables
    var canvasx = $(canvas).offset().left;
    var canvasy = $(canvas).offset().top;
    var last_mousex = last_mousey = 0;
    var mousex = mousey = 0;
    var mousedown = false;

    var ax = ay = bx = by = 0;
    var zones = [];

    var image = document.getElementById("im");

    function drawImageScaled(img, ctx) {
        var hRatio = canvas.width  / img.width    ;
        var vRatio =  canvas.height / img.height  ;
        var ratio  = Math.min ( hRatio, vRatio );
        var centerShift_x = ( canvas.width - img.width*ratio ) / 2;
        var centerShift_y = ( canvas.height - img.height*ratio ) / 2;
        ctx.clearRect(0,0,canvas.width, canvas.height);
        ctx.drawImage(img, 0,0, img.width, img.height,
            centerShift_x,centerShift_y,img.width*ratio, img.height*ratio);
    }

    drawImageScaled(image, ctx);
    document.onload = function(){drawImageScaled(image, ctx);};
    //Mousedown
    $(canvas).on('mousedown', function(e) {
        last_mousex = parseInt(e.pageX-canvasx);
        last_mousey = parseInt(e.pageY-canvasy);
        mousedown = true;
        ax = e.pageX-canvasx;
        ay = e.pageY-canvasy;
    });

    //Mouseup
    $(canvas).on('mouseup', function(e) {
        refreshCanvas();
        bx = e.pageX-canvasx;
        by = e.pageY-canvasy;

        mousedown = false;
    });

    //Mousemove
    $(canvas).on('mousemove', function(e) {
        refreshCanvas();
        mousex = parseInt(e.pageX-canvasx);
        mousey = parseInt(e.pageY-canvasy);
        if(mousedown) {
            ctx.clearRect(0,0,canvas.width,canvas.height); //clear canvas
            ctx.beginPath();
            var width = mousex-last_mousex;
            var height = mousey-last_mousey;
            drawImageScaled(image, ctx);
            zones=[last_mousex,last_mousey,Math.sqrt(Math.pow(mousex-last_mousex,2)+Math.pow(mousey-last_mousey,2))];
            ctx.arc(last_mousex,last_mousey, Math.sqrt(Math.pow(mousex-last_mousex,2)+Math.pow(mousey-last_mousey,2)),0,2*Math.PI);
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
        //Output
        $('#position').attr('value',zones);
    });

    function effacer() {
        ctx.clearRect(0,0,canvas.width,canvas.height);
        drawImageScaled(image, ctx);
        $('#position').attr('value','');
        zones=[];

    }


    function refreshCanvas() {
        canvasx = $(canvas).offset().left;
        canvasy = $(canvas).offset().top;
    }