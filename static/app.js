(function() {

    function showProgress() {
        $("#messages").append("<div class='progress'><span style='width:0%;' class='meter'></span></div>");

        $(".meter").animate({width:"50%"}, 3000);
    }

    function showProgressComplete() {
        $(".meter").animate({width:"100%"});
        setTimeout(function() {
            $("#messages").empty();
        }, 100);
    }

    // success callback for visualization
    function displaySuccess(response) {
        console.log("display success");

        // complete progress bar
        showProgressComplete();
        // re-enable button
        $("#visualize").removeClass("disabled");

        // add #detail sidebar
        $("#detail-container").append("<div class='panel' id='detail'><h5> Click the bubbles to see more about your Twitter friends.</h5><ul><li id='tw-handle'></li><li id='score'></li><li id='followers'></li></ul><div id='tweets'></div></div>");

        // call method from data_viz.js
        VIZ.createVisualization(response);
    }

    $("#visualize").on("click", function(e){
        e.preventDefault();
        $(this).addClass("disabled");

        // store screen name
        var screen_name = $("input[name=screen_name]").val();
        // first-pass validation: make sure screen_name is not blank
        if (screen_name.length > 0) {
            console.log(screen_name);
            // add progress bar
            showProgress();

            // make AJAX request, using success callback
            TwitterAjax.callDisplay(screen_name, displaySuccess);

        }
        else {
            $("#messages").empty().text("Please enter a valid Twitter handle!");
        }
    });




})();

