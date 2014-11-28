(function() {

    $("#visualize").click(function(e){
        e.preventDefault();
        var screen_name = $("input[name=screen_name]").val();
        if (screen_name.length > 0) {
            console.log(screen_name);
            $("#messages").append("<div class='progress'><span class='meter'></span></div>");

            function displaySuccess(response) {
                console.log("display success");
                $("#detail-container").append("<div class='panel' id='detail'><h5> Click the bubbles to see more about your Twitter friends.</h5><ul></ul><div id='tweets'></div></div>");
                VIZ.createVisualization(response);
            }

            TwitterAjax.callDisplay(screen_name, displaySuccess);

        }
        else {
            $("#result").text("Please enter a valid Twitter handle!");
        }
    });

    var progressBar = $('.progress');               // Variable to cache progress bar element
    var progressBarMeter = $('.progress .meter');   // Variable to cache meter element


})();

