(function() {

    // progress bar controls
    function showProgress() {
        $("#messages").append("<div class='progress'><span style='width:0%;' class='meter'></span></div>");

        $(".meter").animate({width:"50%"}, 3000);
    }

    function showProgressComplete() {
        $(".meter").animate({width:"100%"});
        setTimeout(function() {
            $(".progress").remove();
        }, 100);
    }

    function addVizHeadline(screenName) {
        $("#viz h2").remove();
        $("#viz").prepend("<h2>@" + screenName + "'s Twitter Friends" + "</h2>");
    }

    // success callback for visualization
    function displaySuccess(response) {
        // clear svg in case previous visualization exists
        $("svg").remove()
        // re-enable button
        $("#visualize").removeClass("disabled");
        // show sidebar
        $("#detail").removeClass("hidden");
        // complete and remove progress bar
        showProgressComplete();
        // add header above visualization
        addVizHeadline(response["name"]);

        // create visualization in data_viz.js
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

