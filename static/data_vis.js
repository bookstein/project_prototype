/*
  VIZ acts as the namespace for all functions related to d3 and visualization interactivity.

  showTweets: loads a given user's timeline using Twitter widget
    @params: screen name
    @returns: Twitter widget showing user's recent tweets embedded in #tweets div

  createVisualization: creates svg and all related elements using the JSON response from server.
    @params: JSON of user screen names, number of followers, and their politicalness scores.
    @returns: d3 packed bubble chart

*/
var VIZ = VIZ || (function () {

  function showTweets(screenName) {
    $("#tweets").empty()

    // embeds a timeline in #tweets div
    twttr.ready(
      function (twttr) {
        twttr.widgets.createTimeline(

          // FIXME: this should be private
          // widget id
          '538087329949548544',

          // $ returns jQuery obj, get first elem [0] in obj
          $('#tweets')[0],
          {
            tweetLimit: 3,
            screenName: screenName,
            showReplies: "false",
          });
      });
  }

  return {

    createVisualization: function(scores) {

      margin = 10;

      // set diameter of bubble pack
      var diameter = $("#viz").width() - margin,
      format = d3.format(",d");

      var bubble = d3.layout.pack()
          .sort( function(a, b) {

            // sort bubbles in reverse order of score
            return -(a.score - b.score);

          })
          .size([diameter, diameter])
          .padding(2);

      // append svg to #viz div
      var svg = d3.select("#viz").append("svg")
          .attr("width", diameter)
          .attr("height", diameter)
          .attr("class", "bubble");

      // rename JSON response object to 'root' for classes function to work
      var root = scores;

      var node = svg.selectAll(".node")
        .data(bubble.nodes(classes(root))
        .filter(function(d) { return !d.children; }))
      .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

      node.append("circle")
          .attr("r", function(d) { return d.r; })
          .attr("fill", function(d) {

            // opacity is a function of political score
            // TODO: make this color setting a variable, to stay DRY
            return "rgba(85,26,139, " + d.score + ")";
          });

      node.append("text")
        .text(function(d) {
          return d.className.substring(0, d.r / 3)
        })
        .style("font-size", function(d) {
          return Math.min(2 * d.r, (2 * d.r - 8) / this.getComputedTextLength() * 10) + "px";
        })
        .attr("dy", ".3em");


      node.on("mouseover", function(d) {

        // TODO: change mouse into pointer on hover

        // Update data values in #detail panel list
        $("#tw-handle").text("@" + d.className);
        $("#score").text("Political tweets: " + parseInt( d.score * 100 ) + "%");
        $("#followers").text("Followers: " + d.value);

      });

      node.on("click", function(d) {

        showTweets(d.className);

      });


      /*
      This function returns a flattened hierarchy containing all leaf nodes under the root.

      From Mbostock's bl.ocks example of flattened bubble graph.

        @params: object containing multi-level hierarchy
        @returns an object that moved all children in the hierarchy into a single non-hierarchical list.
      */
      function classes(root) {

        // keep variable names as packageName, className, value, and score -- otherwise cannot generated numeric values for x,y,r

        var classes = [];

        function recurse(name, node) {
          if (node.children) node.children.forEach(function(child) {
            recurse(node.name, child);
          });
          else classes.push({packageName: name, className: node.name, value: node.size, score: node.score});
        }

        recurse(null, root);

        return {children: classes};
      }

    }
  }

})();



