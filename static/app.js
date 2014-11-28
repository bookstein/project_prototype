(function() {

    $("#visualize").click(function(e){
        e.preventDefault();
        // store screen name
        var screen_name = $("input[name=screen_name]").val();
        // first-pass validation: make sure screen_name is not blank
        if (screen_name.length > 0) {
            console.log(screen_name);
            // add progress bar
            $("#messages").append("<div class='progress'><span class='meter'></span></div>");

            // success callback
            function displaySuccess(response) {
                console.log("display success");
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

    var progressBar = $('.progress');               // Variable to cache progress bar element
    var progressBarMeter = $('.progress .meter');   // Variable to cache meter element

    // $(submitButton).click(function() { // Initiates the send interaction
    // $(this).fadeOut(500); // Fades out submit button when it's clicked
    // setTimeout(function() { // Delays the next effect
    //     $(progressBar).fadeIn(500); // Fades in the progress bar
    //     $(progressBarMeter).animate({width : '100%'},2000); // Animates the progress bar
    //     setTimeout(function() { // Delays the next effect
    //         $(progressBar).fadeOut(500); // Fades out progress bar when animation completes
    //         setTimeout(function() { // Delays the next effect
    //              $(alertBox).fadeIn(500); // Fades in success alert
    //         }, 500);
    //     }, 2500);
    // }, 500);
// });


})();

