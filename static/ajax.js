var TwitterAjax = TwitterAjax || (function() {

    function ajaxFunc (url) {
        // returns a function that calls my Flask server at given url
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

    // callDisplay is a function that takes a success callback
        callDisplay: ajaxFunc("/get/user"),

        getTweets: ajaxFunc("/tweets")

    }


})();


