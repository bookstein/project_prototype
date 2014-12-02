/*
  My AJAX library.
  Adding addition AJAX calls is easy to do and to maintain -- simply add to the returned object.
*/
var TwitterAjax = TwitterAjax || (function() {

  /*
    createAjax builds AJAX requests given a url.

    @params: url that corresponds to a Flask route
    @returns: a function that takes 2 parameters (screen name, success callback) and outputs the success callback's return value.
  */
  function createAjax (url) {

    // returns a function that calls my Flask server at a given url
    return (function(screen_name, successCallback) {
        $.ajax({
            url: url,
            data: JSON.stringify({"screen_name":screen_name}),
            type: "POST",
            dataType: 'json',
            contentType: 'application/json;charset=UTF-8',
            success: function(response) {
                successCallback(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
  }

  return {

    // callDisplay creates the AJAX request that initiates getting visualization in app.js
    callDisplay: createAjax("/ajax/user")

  }

})();


