(function() {

    function showProgress() {
        $("#messages").append("<div class='progress'><span style='width:0%;' class='meter'></span></div>");

        $(".meter").animate({width:"50%"});
    }

    function showProgressComplete() {
        $(".meter").animate({width:"100%"}, 1000);
        setTimeout(function() {
            $("#messages").empty();
        }, 100);
    }

    $("#visualize").click(function(e){
        e.preventDefault();
        // store screen name
        var screen_name = $("input[name=screen_name]").val();
        // first-pass validation: make sure screen_name is not blank
        if (screen_name.length > 0) {
            console.log(screen_name);
            // add progress bar
            showProgress();

            // success callback
            function displaySuccess(response) {
                console.log("display success");

                showProgressComplete();

                $("#detail-container").append("<div class='panel' id='detail'><h5> Click the bubbles to see more about your Twitter friends.</h5><ul></ul><div id='tweets'></div></div>");
                VIZ.createVisualization(response);
            }

            // make initial AJAX request, using success callback
            TwitterAjax.callDisplay(screen_name, displaySuccess);

        }
        else {
            $("#messages").empty().text("Please enter a valid Twitter handle!");
        }
    });




})();

