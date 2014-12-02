(function() {

  // progress bar controls
  function showProgress(screenName) {
    $("#messages").append("<h3>Analyzing Twitter friends for @" + screenName + "</h3>").append("<div class='progress'><span style='width:0%;' class='meter'></span></div>");

    $(".meter").animate({width:"50%"}, 3000);
  }

  function showProgressComplete() {
    $(".meter").animate({width:"100%"}, 5);
    $(".progress").remove();
    $("#messages h3").remove();
  }

  function addVizHeadline(screenName) {
    $("#viz").prepend("<h3>@" + screenName + "'s top 50 Twitter friends" + "</h3>");
  }

  function clearPreviousData() {

    // clear svg in case previous visualization exists
    $("svg").remove()

    // empty out #detail panel list items
    $("#detail ul li").empty()

    // clear previous headline
    $("#viz h3").remove();

    // remove timeline from twitter widget
    $("#tweets").empty()
  }

  /*
      success callback calls createVisualization method in data_viz.js
      @param response: JSON response from Flask server
      @return svg element and D3 visualization
  */
  function displaySuccess(response) {

    // re-enable button
    $("#visualize").removeClass("disabled");

    // show sidebar
    $("#detail").removeClass("hidden");

    // show instructions
    $("#instructions").removeClass("hidden");

    // complete and remove progress bar
    showProgressComplete();

    // add header above visualization
    addVizHeadline(response["name"]);

    // create visualization in data_viz.js
    VIZ.createVisualization(response);
  }

  /*
      form submission event handler
      sends form data with AJAX request to Flask
      call displaySuccess on success
  */
  $("form").on("submit", function(e){
    e.preventDefault();

    // disable submit button
    $("#visualize").addClass("disabled");

    // store screen name
    var screenName = $("input[name=screen_name]").val();

    // first-pass validation: remove @, make sure screen_name is not blank
    if (screenName.length > 0) {

        if (screenName[0] === "@") {
            screenName = screenName.slice(1)
        }

        // add progress bar
        showProgress(screenName);

        // clear any previous data
        clearPreviousData();

        // make AJAX request, using success callback
        TwitterAjax.callDisplay(screenName, displaySuccess);

    }

    else {
        $("#messages").empty().text("Please enter a valid Twitter handle!");
    }

  });

})();

