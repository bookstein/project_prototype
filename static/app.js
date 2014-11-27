(function() {

    $("#visualize").click(function(e){
        e.preventDefault();
        var screen_name = $("input[name=screen_name]").val();
        if (screen_name.length > 0) {
            console.log(screen_name);
            $("#messages").append("<div class='progress'><span class='meter'></span></div>");
            function displaySuccess(response) {
                VIZ.createVisualization(response);
            }

            TwitterAjax.callDisplay(screen_name, displaySuccess);
        }
        else {
            $("#result").text("Please enter a valid Twitter handle!");
        }
    });




})();

