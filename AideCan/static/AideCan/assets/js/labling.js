


     $('#ap').change(function () {
         console.log("change");
         console.log(($(this).val() === "NORM"));
         if($(this).val() === "NORM"){
                $("#soa #nul").removeClass("hidden");
                $("#soa #B").removeAttr("selected");
                $("#soa #nul").attr("selected","true")
                $('#B').addClass("hidden");
                $('#M').addClass("hidden");

            }
            else{
                $("#soa #nul").addClass("hidden");
                $("#soa #nul").removeAttr("selected");
                   $("#B").removeClass("hidden");
                   $("#M").removeClass("hidden");

                $("#soa #B").attr("selected","true");


            }

        });

